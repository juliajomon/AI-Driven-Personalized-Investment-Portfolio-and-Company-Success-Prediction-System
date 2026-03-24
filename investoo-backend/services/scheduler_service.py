from database.portfolio_repository import get_saved_portfolios
from database.alert_repository import create_alert


def check_saved_portfolios():

    portfolios = get_saved_portfolios()

    for p in portfolios:

        old_return = p["expected_return"]

        # placeholder calculation
        new_return = old_return

        if abs(new_return - old_return) > 0.05:

            create_alert(
                p["user_id"],
                p["id"],
                "Your saved portfolio performance changed significantly."
            )