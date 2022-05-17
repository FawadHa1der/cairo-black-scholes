import asyncio
import os
import random
import pytest
import numpy
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.analytical import vega, d1, d2, delta, gamma, theta, rho

from starkware.starknet.compiler.compile import compile_starknet_files
from starkware.starknet.testing.starknet import Starknet

# The path to the contract source code.
CONTRACT_FILE = os.path.join(
    os.path.dirname(__file__), "black_scholes_contract.cairo")

# Precision used in the black scholes Cairo library.
CAIRO_PRIME = 3618502788666131213697322783095070105623107215331596699973092056135872020481
CAIRO_PRIME_HALF = CAIRO_PRIME//2

UNIT = 1e27


def get_lift(x):
    print('get_lift %d:' % x)
    if x < CAIRO_PRIME_HALF:
        print('less than half prime %d:' % CAIRO_PRIME_HALF)
    else:
        print('returning  %d:' % (x - CAIRO_PRIME))

    return x if x < CAIRO_PRIME_HALF else x - CAIRO_PRIME


def get_precise(value):
    return int(UNIT * value)

# Checks accuracy of the option price (within $0.01).


def check_price(got, expected):
    assert(abs(got - expected) < 0.01)

# Returns a random tuple of (t_annualised, volatility, spot, strike, rate)


def get_random_test_input():
    # Random time from 10 minutes to 5 years.
    t_annualised = random.uniform(1/52560.0, 5)
    # Random volatility from 0.01% to 50%.
    volatility = random.uniform(0.0001, 0.5)
    # Random spot price between $0.01 and $1000
    spot = random.uniform(0.01, 1000)
    # Random strike price between $0.01 and $1000
    strike = random.uniform(0.01, 1000)
    # Random interest rate between 0.01% and 50%
    rate = random.uniform(0.0001, 0.5)
    return (t_annualised, volatility, spot, strike, rate)


# @pytest.mark.asyncio
# async def test_randomized_black_scholes_options_prices():
#     # Create a new Starknet class that simulates the StarkNet system.
#     starknet = await Starknet.empty()

#     # Deploy the contract.
#     contract_def = compile_starknet_files(files=[CONTRACT_FILE],
#                                           disable_hint_validation=True)
#     contract = await starknet.deploy(
#         contract_def=contract_def,
#     )

#     # Number of random tests to run.
#     ITERATIONS = 10

#     # List of float tuple (t_annualised, volatility, spot, strike, rate).
#     test_inputs = []

#     # Query the contract for options prices.
#     tasks = []
#     for i in range(ITERATIONS):
#         test_input = get_random_test_input()
#         test_inputs.append(test_input)
#         tasks.append(contract.option_prices(
#             t_annualised=get_precise(test_input[0]),
#             volatility=get_precise(test_input[1]),
#             spot=get_precise(test_input[2]),
#             strike=get_precise(test_input[3]),
#             rate=get_precise(test_input[4])).call())

#     # Compare call and put prices with the python black scholes library.
#     print()
#     execution_infos = await asyncio.gather(*tasks)
#     for i, execution_info in enumerate(execution_infos):
#         (got_call, got_put) = (execution_info.result.call_price/UNIT,
#                                execution_info.result.put_price/UNIT)

#         (exp_call, exp_put) = (
#             black_scholes('c', test_inputs[i][2], test_inputs[i][3],
#                           test_inputs[i][0], test_inputs[i][4],
#                           test_inputs[i][1]),
#             black_scholes('p', test_inputs[i][2], test_inputs[i][3],
#                           test_inputs[i][0], test_inputs[i][4],
#                           test_inputs[i][1]))

#         print()
#         print('Input %d:' % i)
#         print('t_annualised: %.5f years' % test_inputs[i][0])
#         print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
#         print('spot price: $%.5f' % test_inputs[i][2])
#         print('strike price: $%.5f' % test_inputs[i][3])
#         print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
#         print()
#         print('Result %d:' % i)
#         print('Computed call price: $%0.5f, Expected call price: $%0.5f' % (
#             got_call, exp_call))
#         print('Computed put price: $%0.5f, Expected put price: $%0.5f' % (
#             got_put, exp_put))


# @pytest.mark.asyncio
# async def test_randomized_black_scholes_theta():
#     # Create a new Starknet class that simulates the StarkNet system.
#     starknet = await Starknet.empty()

#     # Deploy the contract.
#     contract_def = compile_starknet_files(files=[CONTRACT_FILE],
#                                           disable_hint_validation=True)
#     contract = await starknet.deploy(
#         contract_def=contract_def,
#     )

#     # Number of random tests to run.
#     ITERATIONS = 10

#     # List of float tuple (t_annualised, volatility, spot, strike, rate).
#     test_inputs = []

#     # Query the contract for options prices.
#     tasks = []
#     for i in range(ITERATIONS):
#         test_input = get_random_test_input()
#         test_inputs.append(test_input)
#         tasks.append(contract.theta(
#             t_annualised=get_precise(test_input[0]),
#             volatility=get_precise(test_input[1]),
#             spot=get_precise(test_input[2]),
#             strike=get_precise(test_input[3]),
#             rate=get_precise(test_input[4])).call())

#     # Compare call and put prices with the python black scholes library.
#     print()
#     execution_infos = await asyncio.gather(*tasks)
#     for i, execution_info in enumerate(execution_infos):
#         (got_call, got_put) = (get_lift(execution_info.result.call_theta)/UNIT,
#                                get_lift(execution_info.result.put_theta)/UNIT)

#         (exp_call, exp_put) = (
#             theta('c', test_inputs[i][2], test_inputs[i][3],
#                   test_inputs[i][0], test_inputs[i][4],
#                   test_inputs[i][1]),
#             theta('p', test_inputs[i][2], test_inputs[i][3],
#                   test_inputs[i][0], test_inputs[i][4],
#                   test_inputs[i][1]))

#         print()
#         print('Input %d:' % i)
#         print('t_annualised: %.5f years' % test_inputs[i][0])
#         print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
#         print('spot price: $%.5f' % test_inputs[i][2])
#         print('strike price: $%.5f' % test_inputs[i][3])
#         print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
#         print()
#         print('Result %d:' % i)
#         print('Computed call theta: $%0.5f, Expected call theta: $%0.5f' % (
#             got_call, exp_call))
#         print('Computed put theta: $%0.5f, Expected put theta: $%0.5f' % (
#             got_put, exp_put))

#         check_price(got_call, exp_call)
#         check_price(got_put, exp_put)


# @ pytest.mark.asyncio
# async def test_randomized_black_scholes_vega():
#     # Create a new Starknet class that simulates the StarkNet system.
#     starknet = await Starknet.empty()

#     # Deploy the contract.
#     contract_def = compile_starknet_files(files=[CONTRACT_FILE],
#                                           disable_hint_validation=True)
#     contract = await starknet.deploy(
#         contract_def=contract_def,
#     )

#     # Number of random tests to run.
#     ITERATIONS = 10

#     # List of float tuple (t_annualised, volatility, spot, strike, rate).
#     test_inputs = []

#     # Query the contract for options prices.
#     tasks = []
#     for i in range(ITERATIONS):
#         test_input = get_random_test_input()
#         test_inputs.append(test_input)
#         tasks.append(contract.vega(
#             t_annualised=get_precise(test_input[0]),
#             volatility=get_precise(test_input[1]),
#             spot=get_precise(test_input[2]),
#             strike=get_precise(test_input[3]),
#             rate=get_precise(test_input[4])).call())

#     # Compare call and put prices with the python black scholes library.
#     print()
#     execution_infos = await asyncio.gather(*tasks)
#     for i, execution_info in enumerate(execution_infos):
#         # the library expects it be multiplied by .01
#         (got_call) = ((get_lift(execution_info.result.vega)/UNIT) * .01)

#         (exp_call) = (
#             vega('c', test_inputs[i][2], test_inputs[i][3],
#                  test_inputs[i][0], test_inputs[i][4],
#                  test_inputs[i][1]))

#         print()
#         print('Input %d:' % i)
#         print('t_annualised: %.5f years' % test_inputs[i][0])
#         print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
#         print('spot price: $%.5f' % test_inputs[i][2])
#         print('strike price: $%.5f' % test_inputs[i][3])
#         print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
#         print()
#         print('Result %d:' % i)
#         print('Computed vega: $%0.5f, Expected vega: $%0.5f' % (
#             got_call, exp_call))

#         check_price(got_call, exp_call)

# @ pytest.mark.asyncio
# async def test_randomized_black_scholes_gamma():
#     # Create a new Starknet class that simulates the StarkNet system.
#     starknet = await Starknet.empty()

#     # Deploy the contract.
#     contract_def = compile_starknet_files(files=[CONTRACT_FILE],
#                                           disable_hint_validation=True)
#     contract = await starknet.deploy(
#         contract_def=contract_def,
#     )

#     # Number of random tests to run.
#     ITERATIONS = 10

#     # List of float tuple (t_annualised, volatility, spot, strike, rate).
#     test_inputs = []

#     # Query the contract for options prices.
#     tasks = []
#     for i in range(ITERATIONS):
#         test_input = get_random_test_input()
#         test_inputs.append(test_input)
#         tasks.append(contract.gamma(
#             t_annualised=get_precise(test_input[0]),
#             volatility=get_precise(test_input[1]),
#             spot=get_precise(test_input[2]),
#             strike=get_precise(test_input[3]),
#             rate=get_precise(test_input[4])).call())

#     # Compare call and put prices with the python black scholes library.
#     print()
#     execution_infos = await asyncio.gather(*tasks)
#     for i, execution_info in enumerate(execution_infos):
#         # the library expects it be multiplied by .01
#         (got_call) = ((get_lift(execution_info.result.gamma)/UNIT) * .01)

#         (exp_call) = (
#             gamma('c', test_inputs[i][2], test_inputs[i][3],
#                   test_inputs[i][0], test_inputs[i][4],
#                   test_inputs[i][1]))

#         print()
#         print('Input %d:' % i)
#         print('t_annualised: %.5f years' % test_inputs[i][0])
#         print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
#         print('spot price: $%.5f' % test_inputs[i][2])
#         print('strike price: $%.5f' % test_inputs[i][3])
#         print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
#         print()
#         print('Result %d:' % i)
#         print('Computed gamma: $%0.5f, Expected gamma: $%0.5f' % (
#             got_call, exp_call))

#         check_price(got_call, exp_call)


# @pytest.mark.asyncio
# async def test_randomized_black_scholes_delta():
#     # Create a new Starknet class that simulates the StarkNet system.
#     starknet = await Starknet.empty()

#     # Deploy the contract.
#     contract_def = compile_starknet_files(files=[CONTRACT_FILE],
#                                           disable_hint_validation=True)
#     contract = await starknet.deploy(
#         contract_def=contract_def,
#     )

#     # Number of random tests to run.
#     ITERATIONS = 10

#     # List of float tuple (t_annualised, volatility, spot, strike, rate).
#     test_inputs = []

#     # Query the contract for options prices.
#     tasks = []
#     for i in range(ITERATIONS):
#         test_input = get_random_test_input()
#         test_inputs.append(test_input)
#         tasks.append(contract.delta(
#             t_annualised=get_precise(test_input[0]),
#             volatility=get_precise(test_input[1]),
#             spot=get_precise(test_input[2]),
#             strike=get_precise(test_input[3]),
#             rate=get_precise(test_input[4])).call())

#     # Compare call and put prices with the python black scholes library.
#     print()
#     execution_infos = await asyncio.gather(*tasks)
#     for i, execution_info in enumerate(execution_infos):
#         (got_call, got_put) = (get_lift(execution_info.result.call_delta)/UNIT,
#                                get_lift(execution_info.result.put_delta)/UNIT)

#         (exp_call, exp_put) = (
#             delta('c', test_inputs[i][2], test_inputs[i][3],
#                   test_inputs[i][0], test_inputs[i][4],
#                   test_inputs[i][1]),
#             delta('p', test_inputs[i][2], test_inputs[i][3],
#                   test_inputs[i][0], test_inputs[i][4],
#                   test_inputs[i][1]))

#         print()
#         print('Input %d:' % i)
#         print('t_annualised: %.5f years' % test_inputs[i][0])
#         print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
#         print('spot price: $%.5f' % test_inputs[i][2])
#         print('strike price: $%.5f' % test_inputs[i][3])
#         print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
#         print()
#         print('Result %d:' % i)
#         print('Computed call delta: $%0.5f, Expected call delta: $%0.5f' % (
#             got_call, exp_call))
#         print('Computed put delta: $%0.5f, Expected put delta: $%0.5f' % (
#             got_put, exp_put))

#         check_price(got_call, exp_call)
#         check_price(got_put, exp_put)


def Vanna_(S, K, T, r, sigma):
    lista = []
    d1 = (numpy.log(S / K) + (r + 1/2 * sigma ** 2) * T) / \
        (sigma * numpy.sqrt(T))
    d2 = d1-sigma*T**(1/2)
    return (1 / numpy.sqrt(2 * numpy.pi) * S * numpy.exp(-d1 ** 2 * 1/2) * numpy.sqrt(T))/S * (1 - d1/(sigma*numpy.sqrt(T)))


@pytest.mark.asyncio
async def test_randomized_black_scholes_vanna():
    # Create a new Starknet class that simulates the StarkNet system.
    starknet = await Starknet.empty()

    # Deploy the contract.
    contract_def = compile_starknet_files(files=[CONTRACT_FILE],
                                          disable_hint_validation=True)
    contract = await starknet.deploy(
        contract_def=contract_def,
    )

    # Number of random tests to run.
    ITERATIONS = 10

    # List of float tuple (t_annualised, volatility, spot, strike, rate).
    test_inputs = []

    # Query the contract for options prices.
    tasks = []
    for i in range(ITERATIONS):
        test_input = get_random_test_input()
        test_inputs.append(test_input)
        tasks.append(contract.vanna(
            t_annualised=get_precise(test_input[0]),
            volatility=get_precise(test_input[1]),
            spot=get_precise(test_input[2]),
            strike=get_precise(test_input[3]),
            rate=get_precise(test_input[4])).call())

    # Compare call and put prices with the python black scholes library.
    print()
    execution_infos = await asyncio.gather(*tasks)
    for i, execution_info in enumerate(execution_infos):
        (got_call) = (get_lift(execution_info.result.vanna)/UNIT)

        (exp_call) = Vanna_(test_inputs[i][2], test_inputs[i][3],
                            test_inputs[i][0], test_inputs[i][4],
                            test_inputs[i][1])

        print()
        print('Input %d:' % i)
        print('t_annualised: %.5f years' % test_inputs[i][0])
        print('volatility: %.5f%%' % (100 * test_inputs[i][1]))
        print('spot price: $%.5f' % test_inputs[i][2])
        print('strike price: $%.5f' % test_inputs[i][3])
        print('interest rate: %.5f%%' % (100 * test_inputs[i][4]))
        print()
        print('Result %d:' % i)
        print('Computed vanna: $%0.5f, Expected vanna: $%0.5f' % (
            got_call, exp_call))

        check_price(got_call, exp_call)
