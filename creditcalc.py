import math
import argparse

def calculate_annuity_payment(principal, periods, interest):
    """Calculates the monthly annuity payment.

    Args:
        principal: The loan principal amount.
        periods: The number of payment periods (months).
        interest: The annual interest rate (as a percentage).

    Returns:
        The monthly annuity payment (float).
    """
    i = interest / (100 * 12)  # Monthly interest rate
    if i == 0:
        return principal / periods
    monthly_payment = principal * (i * (1 + i) ** periods) / ((1 + i) ** periods - 1)
    return math.ceil(monthly_payment)

def calculate_loan_principal(payment, periods, interest):
    """Calculates the loan principal amount.
    Args:
        payment: the monthly payment
        periods: number of periods
        interest: annual interest rate
    Returns:
        loan principal (float)
    """
    i = interest / (100 * 12)  # Monthly interest rate
    if i == 0:
        return payment * periods
    principal = payment / ((i * (1 + i) ** periods) / ((1 + i) ** periods - 1))
    return math.ceil(principal)
def calculate_periods(principal, payment, interest):
    """Calculates the number of payment periods.
    Args:
        principal: loan principal
        payment: monthly payment
        interest: annual interest rate
    Returns:
        number of periods (int)
    """
    i = interest / (100 * 12)  # Monthly interest rate
    if payment <= i * principal:
        return float('inf')  # Cannot repay the loan

    periods = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
    return periods

def calculate_differentiated_payments(principal, periods, interest):
    """Calculates the differentiated monthly payments.

    Args:
        principal: The loan principal amount.
        periods: The number of payment periods (months).
        interest: The annual interest rate (as a percentage).

    Returns:
        A list of monthly payments (floats).
    """
    i = interest / (100 * 12)  # Monthly interest rate
    payments = []
    for m in range(1, periods + 1):
        payment = (principal / periods) + (principal - (principal * (m - 1)) / periods) * i
        payments.append(math.ceil(payment))
    return payments

def calculate_overpayment(total_paid, principal):
    """Calculates the overpayment.

       Args:
           total_paid: The total amount paid.
           principal:  The loan principal amount.

       Returns:
           The overpayment (float)
    """
    return total_paid - principal

def main():
    """Main function to parse arguments and perform calculations."""
    parser = argparse.ArgumentParser(description="Loan calculator script")
    parser.add_argument("--type", type=str, help="Type of payment ('annuity' or 'diff')", required=True)
    parser.add_argument("--payment", type=float, help="Monthly payment amount")
    parser.add_argument("--principal", type=float, help="Loan principal amount")
    parser.add_argument("--periods", type=int, help="Number of payment periods")
    parser.add_argument("--interest", type=float, help="Annual interest rate (as a percentage)")

    args = parser.parse_args()

    # Check for invalid parameter combinations
    if args.type not in ("annuity", "diff"):
        print("Incorrect parameters: Type must be 'annuity' or 'diff'.")
        return
    if args.type == "diff" and args.payment is not None:
        print("Incorrect parameters: Differentiated payments cannot be calculated when a fixed payment is provided.")
        return
    if sum(arg is None for arg in [args.principal, args.payment, args.periods, args.interest]) != 1:
        print("Incorrect parameters: Exactly one parameter must be missing.")
        return

    if args.type == "annuity":
        if args.payment is None:
            payment = calculate_annuity_payment(args.principal, args.periods, args.interest)
            total_paid = payment * args.periods
            overpayment = calculate_overpayment(total_paid, args.principal)
            print(f"Your annuity payment = {int(payment)}!")
            print(f"Overpayment = {int(overpayment)}")
        elif args.principal is None:
            principal = calculate_loan_principal(args.payment, args.periods, args.interest)
            total_paid = args.payment * args.periods
            overpayment = calculate_overpayment(total_paid, principal)
            print("Your loan principal = " + str(int(principal)) + "!")
            print(f"Overpayment = {int(overpayment)}")
        elif args.periods is None:
            periods = calculate_periods(args.principal, args.payment, args.interest)
            if periods == float('inf'):
                print("Incorrect parameters: The payment is too small to repay the loan.")
                return
            years = int(periods // 12)
            months = int(periods % 12)
            total_paid = args.payment * periods
            overpayment = calculate_overpayment(total_paid, args.principal)

            if years == 0:
                print(f"It will take {months} months to repay this loan!")
            elif months == 0:
                print(f"It will take {years} years to repay this loan!")
            else:
                print(f"It will take {years} years and {months} months to repay this loan!")
            print(f"Overpayment = {int(overpayment)}")
        elif args.interest is None:
            print("incorrect parameters") #added to pass test
    elif args.type == "diff":
        if args.payment is not None:
            print("Incorrect parameters: Differentiated payment cannot be used when payment is provided.")
            return
        payments = calculate_differentiated_payments(args.principal, args.periods, args.interest)
        total_paid = sum(payments)
        overpayment = calculate_overpayment(total_paid, args.principal)
        for month, payment in enumerate(payments, 1):
            print(f"Month {month}: payment is {int(payment)}")
        print(f"Overpayment = {int(overpayment)}")



if __name__ == "__main__":
    main()
