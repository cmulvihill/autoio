""" Tests the writing of the energy transfer section
"""

import mess_io.writer
from _util import read_text_file


# Core Data
GEO1 = (
    ('C', (-1.4283035320563338, 0.013425343735546437, -0.030302158896694683)),
    ('C', (1.4283027358735494, -0.013425597530894248, 0.0303022919384165)),
    ('H', (-2.1972722614281355, -0.19229727219177065, 1.8778380427620682)),
    ('H', (-2.121310184939721, 1.792702413487708, -0.8231106338374065)),
    ('H', (-2.1448124562913287, -1.5396513482615042, -1.191852168914227)),
    ('H', (2.1448121742707795, 1.539654946791746, 1.1918517388178247)),
    ('H', (2.1972712765396953, 0.1922944277301287, -1.8778395029874426)),
    ('H', (2.121312248031497, -1.7927029137609576, 0.8231123911174519)))
GEO2 = (
    ('O', (-2.4257421043, 6.0797867203, 0.0000000000)),
    ('H', (-0.8184039622, 5.1215269111, 0.0000000000)))
SYM_FACTOR1 = 3.0
SYM_FACTOR2 = 1.0
INTERP_EMAX = 1500
QUANT_LVL_EMAX = 11
POT_SURF_FILE = 'surf.dat'
FLUX_FILE = 'flux.dat'
STOICH = 'C2O1H7'
POT_PREFACTOR = 12.0
POT_EXP = 4.0
TSTLVL = 'ej'

# Rotor Data
HR_GROUP = (6, 7, 8, 9, 10, 11)
HR_AXIS = (2, 3)
HR_SYMMETRY = 1.0
HR_ID = 'D5'
HR_GRID_SIZE = 100
HR_MASS_EXP_SIZE = 5
THERM_POW_MAX = 50.0
LVL_ENE_MAX = 1000.0
POT_EXP_SIZE = 7
HMIN = 15
HMAX = 110
UMBR_GROUP = (4, 5, 6)
UMBR_PLANE = (4, 5, 6)
UMBR_REF = 4
ONEDPOT = {(0,): 0.00, (1,): 2.91, (2,): 9.06, (3,): 12.63,
           (4,): 9.97, (5,): 3.51, (6,): 0.03, (7,): 3.49,
           (8,): 9.96, (9,): 12.63, (10,): 9.08, (11,): 2.93}
REMDUMMY = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1)

# MDHR Data
FLST = (10., 50., 100., 200., 300., 400., 500., 600., 700., 800., 900.)
TWODPOT = {(0, 0): 1.0, (0, 1): 2.0, (0, 2): 3.0, (0, 3): 4.0,
           (1, 1): 6.0, (1, 2): 7.0, (1, 3): 8.0,
           (2, 2): 2.1, (2, 3): 3.1,
           (3, 3): 7.1}
TWODFREQ = {(0, 0): FLST, (0, 1): FLST, (0, 2): FLST, (0, 3): FLST,
            (1, 1): FLST, (1, 2): FLST, (1, 3): FLST,
            (2, 2): FLST, (2, 3): FLST,
            (3, 3): FLST}
THREEDPOT = {(0, 0, 0): 1.0, (0, 0, 1): 2.0,
             (0, 0, 2): 3.0, (0, 0, 3): 4.0,
             (0, 1, 0): 1.0, (0, 1, 1): 2.0,
             (0, 1, 2): 3.0, (0, 1, 3): 4.0,
             (0, 2, 0): 1.0, (0, 2, 1): 2.0,
             (0, 2, 2): 3.0, (0, 2, 3): 4.0,
             (0, 3, 0): 1.0, (0, 3, 1): 2.0,
             (0, 3, 2): 3.0, (0, 3, 3): 4.0}
THREEDFREQ = {(0, 0, 0): FLST, (0, 0, 1): FLST,
              (0, 0, 2): FLST, (0, 0, 3): FLST,
              (0, 1, 0): FLST, (0, 1, 1): FLST,
              (0, 1, 2): FLST, (0, 1, 3): FLST,
              (0, 2, 0): FLST, (0, 2, 1): FLST,
              (0, 2, 2): FLST, (0, 2, 3): FLST,
              (0, 3, 0): FLST, (0, 3, 1): FLST,
              (0, 3, 2): FLST, (0, 3, 3): FLST}
FOURDPOT = {(0, 0, 0, 0): 1.0, (0, 0, 0, 1): 2.0,
            (0, 0, 0, 2): 3.0, (0, 0, 0, 3): 4.0,
            (0, 0, 1, 0): 1.0, (0, 0, 1, 1): 2.0,
            (0, 0, 1, 2): 3.0, (0, 0, 1, 3): 4.0,
            (0, 0, 2, 0): 1.0, (0, 0, 2, 1): 2.0,
            (0, 0, 2, 2): 3.0, (0, 0, 2, 3): 4.0,
            (0, 0, 3, 0): 1.0, (0, 0, 3, 1): 2.0,
            (0, 0, 3, 2): 3.0, (0, 0, 3, 3): 4.0,
            (0, 1, 0, 0): 1.0, (0, 1, 0, 1): 2.0,
            (0, 1, 0, 2): 3.0, (0, 1, 0, 3): 4.0,
            (0, 1, 1, 0): 1.0, (0, 1, 1, 1): 2.0,
            (0, 1, 1, 2): 3.0, (0, 1, 1, 3): 4.0,
            (0, 1, 2, 0): 1.0, (0, 1, 2, 1): 2.0,
            (0, 1, 2, 2): 3.0, (0, 1, 2, 3): 4.0,
            (0, 1, 3, 0): 1.0, (0, 1, 3, 1): 2.0,
            (0, 1, 3, 2): 3.0, (0, 1, 3, 3): 4.0,
            (0, 2, 0, 0): 1.0, (0, 2, 0, 1): 2.0,
            (0, 2, 0, 2): 3.0, (0, 2, 0, 3): 4.0,
            (0, 2, 1, 0): 1.0, (0, 2, 1, 1): 2.0,
            (0, 2, 1, 2): 3.0, (0, 2, 1, 3): 4.0,
            (0, 2, 2, 0): 1.0, (0, 2, 2, 1): 2.0,
            (0, 2, 2, 2): 3.0, (0, 2, 2, 3): 4.0,
            (0, 2, 3, 0): 1.0, (0, 2, 3, 1): 2.0,
            (0, 2, 3, 2): 3.0, (0, 2, 3, 3): 4.0,
            (0, 3, 0, 0): 1.0, (0, 3, 0, 1): 2.0,
            (0, 3, 0, 2): 3.0, (0, 3, 0, 3): 4.0,
            (0, 3, 1, 0): 1.0, (0, 3, 1, 1): 2.0,
            (0, 3, 1, 2): 3.0, (0, 3, 1, 3): 4.0,
            (0, 3, 2, 0): 1.0, (0, 3, 2, 1): 2.0,
            (0, 3, 2, 2): 3.0, (0, 3, 2, 3): 4.0,
            (0, 3, 3, 0): 1.0, (0, 3, 3, 1): 2.0,
            (0, 3, 3, 2): 3.0, (0, 3, 3, 3): 4.0}
FOURDFREQ = {(0, 0, 0, 0): FLST, (0, 0, 0, 1): FLST,
             (0, 0, 0, 2): FLST, (0, 0, 0, 3): FLST,
             (0, 0, 1, 0): FLST, (0, 0, 1, 1): FLST,
             (0, 0, 1, 2): FLST, (0, 0, 1, 3): FLST,
             (0, 0, 2, 0): FLST, (0, 0, 2, 1): FLST,
             (0, 0, 2, 2): FLST, (0, 0, 2, 3): FLST,
             (0, 0, 3, 0): FLST, (0, 0, 3, 1): FLST,
             (0, 0, 3, 2): FLST, (0, 0, 3, 3): FLST,
             (0, 1, 0, 0): FLST, (0, 1, 0, 1): FLST,
             (0, 1, 0, 2): FLST, (0, 1, 0, 3): FLST,
             (0, 1, 1, 0): FLST, (0, 1, 1, 1): FLST,
             (0, 1, 1, 2): FLST, (0, 1, 1, 3): FLST,
             (0, 1, 2, 0): FLST, (0, 1, 2, 1): FLST,
             (0, 1, 2, 2): FLST, (0, 1, 2, 3): FLST,
             (0, 1, 3, 0): FLST, (0, 1, 3, 1): FLST,
             (0, 1, 3, 2): FLST, (0, 1, 3, 3): FLST,
             (0, 2, 0, 0): FLST, (0, 2, 0, 1): FLST,
             (0, 2, 0, 2): FLST, (0, 2, 0, 3): FLST,
             (0, 2, 1, 0): FLST, (0, 2, 1, 1): FLST,
             (0, 2, 1, 2): FLST, (0, 2, 1, 3): FLST,
             (0, 2, 2, 0): FLST, (0, 2, 2, 1): FLST,
             (0, 2, 2, 2): FLST, (0, 2, 2, 3): FLST,
             (0, 2, 3, 0): FLST, (0, 2, 3, 1): FLST,
             (0, 2, 3, 2): FLST, (0, 2, 3, 3): FLST,
             (0, 3, 0, 0): FLST, (0, 3, 0, 1): FLST,
             (0, 3, 0, 2): FLST, (0, 3, 0, 3): FLST,
             (0, 3, 1, 0): FLST, (0, 3, 1, 1): FLST,
             (0, 3, 1, 2): FLST, (0, 3, 1, 3): FLST,
             (0, 3, 2, 0): FLST, (0, 3, 2, 1): FLST,
             (0, 3, 2, 2): FLST, (0, 3, 2, 3): FLST,
             (0, 3, 3, 0): FLST, (0, 3, 3, 1): FLST,
             (0, 3, 3, 2): FLST, (0, 3, 3, 3): FLST}


# Tunnel Data
IMAG_FREQ = 2000.0
WELL_DEPTH1 = 10.0
WELL_DEPTH2 = 20.0
CUTOFF_ENE = 3000.0
TUNNEL_FILE = 'tunnel.dat'


def test__core_rigidrotor_writer():
    """ test mess_io.writer.mol_data.core_rigidrotor
    """

    core_rigrot1_str = mess_io.writer.mol_data.core_rigidrotor(
        GEO1, SYM_FACTOR1)

    core_rigrot2_str = mess_io.writer.mol_data.core_rigidrotor(
        GEO1, SYM_FACTOR1,
        interp_emax=INTERP_EMAX)

    assert core_rigrot1_str == read_text_file(
        ['data', 'inp'], 'core_rigrot1.inp')
    assert core_rigrot2_str == read_text_file(
        ['data', 'inp'], 'core_rigrot2.inp')


def test__core_multirotor_writer():
    """ test mess_io.writer.mol_data.rotor_internal
        test mess_io.writer.mol_data.mdhr_data
        test mess_io.writer.mol_data.core_multirotor
    """

    # Internal Rotor Sections
    rotor_int1_str = mess_io.writer.mol_data.rotor_internal(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, HR_GRID_SIZE, HR_MASS_EXP_SIZE)
    rotor_int2_str = mess_io.writer.mol_data.rotor_internal(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, HR_GRID_SIZE, HR_MASS_EXP_SIZE,
        pot_exp_size=POT_EXP_SIZE,
        hmin=HMIN,
        hmax=HMAX,
        remdummy=REMDUMMY,
        geom=GEO1,
        rotor_id=HR_ID)

    assert rotor_int1_str == read_text_file(['data', 'inp'], 'rotor_int1.inp')
    assert rotor_int2_str == read_text_file(['data', 'inp'], 'rotor_int2.inp')

    mdhr_dat_1d_str = mess_io.writer.mol_data.mdhr_data(
        ONEDPOT)
    mdhr_dat_2dfr_str = mess_io.writer.mol_data.mdhr_data(
        TWODPOT, freqs=TWODFREQ, nrot=3)
    mdhr_dat_3dfr_str = mess_io.writer.mol_data.mdhr_data(
        THREEDPOT, freqs=THREEDFREQ, nrot=3)
    mdhr_dat_4dfr_str = mess_io.writer.mol_data.mdhr_data(
        FOURDPOT, freqs=FOURDFREQ, nrot=3)

    assert mdhr_dat_1d_str == read_text_file(
        ['data', 'inp'], 'mdhr_dat_1d.inp')
    assert mdhr_dat_2dfr_str == read_text_file(
        ['data', 'inp'], 'mdhr_dat_2dfr.inp')
    assert mdhr_dat_3dfr_str == read_text_file(
        ['data', 'inp'], 'mdhr_dat_3dfr.inp')
    assert mdhr_dat_4dfr_str == read_text_file(
        ['data', 'inp'], 'mdhr_dat_4dfr.inp')

    # MultiRotor Core Sections
    core_multirot1_str = mess_io.writer.mol_data.core_multirotor(
        GEO1, SYM_FACTOR1, POT_SURF_FILE, rotor_int1_str)
    core_multirot2_str = mess_io.writer.mol_data.core_multirotor(
        GEO1, SYM_FACTOR1, POT_SURF_FILE, rotor_int1_str,
        interp_emax=INTERP_EMAX,
        quant_lvl_emax=QUANT_LVL_EMAX)

    assert core_multirot1_str == read_text_file(
        ['data', 'inp'], 'core_multirot1.inp')
    assert core_multirot2_str == read_text_file(
        ['data', 'inp'], 'core_multirot2.inp')


def test__core_phasespace_writer():
    """ test mess_io.writer.mol_data.core_phasespace
    """

    # Use the writer to create a string for each of the core sections
    core_pst1_str = mess_io.writer.mol_data.core_phasespace(
        GEO1, GEO2, SYM_FACTOR2, STOICH)

    core_pst2_str = mess_io.writer.mol_data.core_phasespace(
        GEO1, GEO2, SYM_FACTOR2, STOICH,
        pot_prefactor=POT_PREFACTOR,
        pot_exp=POT_EXP,
        tstlvl=TSTLVL)

    assert core_pst1_str == read_text_file(['data', 'inp'], 'core_pst1.inp')
    assert core_pst2_str == read_text_file(['data', 'inp'], 'core_pst2.inp')


def test__core_rotd_writer():
    """ test mess_io.writer.mol_data.core_rotd
    """

    core_rotd_str = mess_io.writer.mol_data.core_rotd(
        SYM_FACTOR1, FLUX_FILE, STOICH)

    assert core_rotd_str == read_text_file(['data', 'inp'], 'core_rotd.inp')


def test__rotor_hindered_writer():
    """ test mess_io.writer.mol_data.rotor_hindered
    """

    rotor_hind1_str = mess_io.writer.mol_data.rotor_hindered(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, ONEDPOT)

    rotor_hind2_str = mess_io.writer.mol_data.rotor_hindered(
        HR_GROUP, HR_AXIS, HR_SYMMETRY, ONEDPOT,
        hmin=HMIN,
        hmax=HMAX,
        lvl_ene_max=LVL_ENE_MAX,
        therm_pow_max=THERM_POW_MAX,
        remdummy=REMDUMMY,
        geom=GEO1,
        rotor_id=HR_ID)

    assert rotor_hind1_str == read_text_file(
        ['data', 'inp'], 'rotor_hind1.inp')
    assert rotor_hind2_str == read_text_file(
        ['data', 'inp'], 'rotor_hind2.inp')


def test__umbrella_writer():
    """ test mess_io.writer.mol_data.umbrella
    """

    umbrella1_str = mess_io.writer.mol_data.umbrella_mode(
        UMBR_GROUP, UMBR_PLANE, UMBR_REF, ONEDPOT)
    umbrella2_str = mess_io.writer.mol_data.umbrella_mode(
        UMBR_GROUP, UMBR_PLANE, UMBR_REF, ONEDPOT,
        remdummy=REMDUMMY,
        geom=GEO1)

    assert umbrella1_str == read_text_file(['data', 'inp'], 'umbrella1.inp')
    assert umbrella2_str == read_text_file(['data', 'inp'], 'umbrella2.inp')


def test__tunnel_eckart_writer():
    """ test mess_io.writer.mol_data.tunnel_eckart
    """

    tunnel_eckart_str = mess_io.writer.mol_data.tunnel_eckart(
        IMAG_FREQ, WELL_DEPTH1, WELL_DEPTH2)

    assert tunnel_eckart_str == read_text_file(
        ['data', 'inp'], 'tunnel_eckart.inp')


def test__tunnel_sct_writer():
    """ test mess_io.writer.mol_data.tunnel_sct
    """

    tunnel_sct1_str = mess_io.writer.mol_data.tunnel_sct(
        IMAG_FREQ, TUNNEL_FILE)
    tunnel_sct2_str = mess_io.writer.mol_data.tunnel_sct(
        IMAG_FREQ, TUNNEL_FILE, cutoff_energy=CUTOFF_ENE)

    assert tunnel_sct1_str == read_text_file(
        ['data', 'inp'], 'tunnel_sct1.inp')
    assert tunnel_sct2_str == read_text_file(
        ['data', 'inp'], 'tunnel_sct2.inp')


if __name__ == '__main__':
    test__core_rigidrotor_writer()
    test__core_multirotor_writer()
    test__core_phasespace_writer()
    test__core_rotd_writer()
    test__rotor_hindered_writer()
    test__umbrella_writer()
    test__tunnel_eckart_writer()
    test__tunnel_sct_writer()