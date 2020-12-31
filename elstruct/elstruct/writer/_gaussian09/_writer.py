""" gaussian09 writer module """

import os
import automol
from ioformat import build_mako_str
import autowrite as aw
import elstruct.par
import elstruct.option
from elstruct import template
from elstruct import pclass
from elstruct.writer. import fill
from elstruct.writer._gaussian09 import par as prog_par


PROG = elstruct.par.Program.GAUSSIAN09

# set the path to the template files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')


def write_input(job_key, geo, charge, method, basis, geo, mult, charge,
                         orb_restricted, mol_options, memory, comment,
                         machine_options,
                         scf_options, casscf_options, corr_options,
                         job_options=(), frozen_coordinates=(),
                         saddle=False,
                         gen_lines=None):
    """ Build a Python dictionary with parameters and values
        that can be used to fill a Mako template for writing
        an electronic structure input file.

        :param job_key: job contained in the inpit file
        :type job_key: str
        :param method: electronic structure method
        :type method: str
        :param basis: basis set
        :type basis: str
        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param mult: spin multiplicity
        :type mult: int
        :param charge: molecular charge
        :type charge: int
        :param orb_restricted: parameter designating if restriced refrence used
        :type orb_restricted: bool
        :param mol_options: options for the molecule block
        :type mol_options: tuple[str]
        ;param memory: memory in GB
        :type memory: int
        :param comment: a comment string to be placed at the top of the file
        :type comment: str
        :param machine_options: machine directives
            (num procs, num threads, etc.)
        :type machine_options: tuple[str]
        :param scf_options: scf method directives
        :type scf_options: tuple[str]
        :param casscf_options: casscf method directives
        :type casscf_options: tuple[str]
        :param corr_options: correlation method directives
        :type corr_options: tuple[str]
        :param job_options: geometry optimization routine directives
        :type job_options: tuple[str]
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :param saddle: optimize a saddle point?
        :type saddle: bool
        :param gen_lines: generic lines for the input file
        :type gen_lines: dict[idx:str]
    """

    reference = _reference(method, mult, orb_restricted)
    geo_str, zmat_var_val_str, zmat_const_val_str = _geometry_strings(
        geo, frozen_coordinates)

    if elstruct.par.Method.is_correlated(method):
        assert not corr_options

    if (reference == par.Reference.ROHF and
            job_key in (JobKey.GRADIENT, JobKey.HESSIAN)):
        job_options = list(job_options)
        job_options.insert(0, 'EnOnly')

    gaussian09_method = elstruct.par.program_method_name(PROG, method)
    gaussian09_basis = elstruct.par.program_basis_name(PROG, basis)

    # in the case of Hartree-Fock, swap the method for the reference name
    if method == elstruct.par.Method.HF[0]:
        gaussian09_method = reference
        reference = ''

    scf_guess_options, scf_options = _intercept_scf_guess_option(scf_options)
    scf_guess_options = _evaluate_options(scf_guess_options)
    scf_options = _evaluate_options(scf_options)
    casscf_options = _evaluate_options(casscf_options)
    job_options = _evaluate_options(job_options)

    if saddle:
        job_options += ('CALCFC', 'TS', 'NOEIGEN', 'MAXCYCLES=60')

    # Set the gen lines blocks
    if gen_lines is not None:
        gen_lines = '\n'.join(gen_lines[1]) if 1 in gen_lines else ''
    else:
        gen_lines = ''

    fill_dct = {
        TemplateKey.MEMORY: memory,
        TemplateKey.MACHINE_OPTIONS: '\n'.join(machine_options),
        TemplateKey.REFERENCE: reference,
        TemplateKey.METHOD: gaussian09_method,
        TemplateKey.BASIS: gaussian09_basis,
        TemplateKey.SCF_OPTIONS: ','.join(scf_options),
        TemplateKey.SCF_GUESS_OPTIONS: ','.join(scf_guess_options),
        TemplateKey.MOL_OPTIONS: ','.join(mol_options),
        TemplateKey.COMMENT: comment,
        TemplateKey.CHARGE: charge,
        TemplateKey.MULT: mult,
        TemplateKey.GEOM: geo_str,
        TemplateKey.ZMAT_VAR_VALS: zmat_var_val_str,
        TemplateKey.ZMAT_CONST_VALS: zmat_const_val_str,
        TemplateKey.JOB_KEY: job_key,
        TemplateKey.JOB_OPTIONS: ','.join(job_options),
        TemplateKey.GEN_LINES: gen_lines,
    }

    return build_mako_str(
        template_file_name='all.mako',
        template_src_path=TEMPLATE_DIR,
        template_keys=fill_dct)


def _geometry_strings(geo, frozen_coordinates):
    """ Build the string for the input geometry

        :param geo: cartesian or z-matrix geometry
        :type geo: tuple
        :param frozen_coordinates: only with z-matrix geometries; list of
            coordinate names to freeze
        :type fozen_coordinates: tuple[str]
        :rtype: (str, str)
    """

    if automol.geom.is_valid(geo):
        geo_str = automol.geom.string(geo)
        zmat_vval_str = ''
        zmat_cval_str = ''
    elif automol.zmatrix.is_valid(geo):
        zma = geo
        symbs = automol.zmatrix.symbols(zma)
        key_mat = automol.zmatrix.key_matrix(zma, shift=1)
        name_mat = automol.zmatrix.name_matrix(zma)
        val_dct = automol.zmatrix.values(zma, angstrom=True, degree=True)
        geo_str = aw.zmatrix.matrix_block(symbs, key_mat, name_mat)

        vval_dct = {key: val for key, val in val_dct.items()
                    if key not in frozen_coordinates}
        cval_dct = {key: val for key, val in val_dct.items()
                    if key in frozen_coordinates}

        zmat_vval_str = aw.zmatrix.setval_block(
            vval_dct, setval_sign=' ').strip()
        zmat_cval_str = aw.zmatrix.setval_block(
            cval_dct, setval_sign=' ').strip()
    else:
        raise ValueError("Invalid geometry value:\n{0}".format(geo))

    return geo_str, zmat_vval_str, zmat_cval_str


def _reference(method, mult, orb_restricted):
    if elstruct.par.Method.is_dft(method):
        reference = ''
    elif mult != 1:
        reference = (prog_par.Reference.ROHF
                     if orb_restricted else prog_par.Reference.UHF)
    else:
        assert mult == 1 and orb_restricted is True
        reference = prog_par.Reference.RHF
    return reference


def _intercept_scf_guess_option(scf_opts):
    guess_opts = []
    ret_scf_opts = []
    for opt in scf_opts:
        if (elstruct.option.is_valid(opt) and opt in
                pclass.values(elstruct.par.Option.Scf.Guess)):
            guess_opts.append(opt)
        else:
            ret_scf_opts.append(opt)
    return guess_opts, ret_scf_opts


def _evaluate_options(opts):
    opts = list(opts)
    for idx, opt in enumerate(opts):
        if elstruct.option.is_valid(opt):
            name = elstruct.option.name(opt)
            assert name in prog_par.OPTION_NAMES
            opts[idx] = prog_par.GAUSSIAN09_OPTION_EVAL_DCT[name](opt)
    return tuple(opts)
