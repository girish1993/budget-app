from itertools import zip_longest


class Category:
    _instance_log = {}

    @classmethod
    def update_instance_log(cls, category, instance):
        if category not in cls._instance_log:
            cls._instance_log[category] = instance

    @classmethod
    def get_category_instance(cls, category):
        return cls._instance_log.get(category)

    def __init__(self, category):
        self._category = category
        self.ledger = []
        Category.update_instance_log(category, self)

    def get_category(self):
        return self._category

    def get_ledger(self):
        return self.ledger

    def add_item_to_ledger(self, item):
        self.ledger.append(item)

    def deposit(self, amount, description=""):
        self.add_item_to_ledger(item={"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount=amount):
            self.add_item_to_ledger(
                {"amount": -abs(amount), "description": description}
            )
            return True
        return False

    def get_balance(self):
        return sum([item["amount"] for item in self.get_ledger()])

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def transfer(self, amount, category):
        if self.check_funds(amount=amount):
            self.withdraw(
                amount=amount, description=f"Transfer to {category.get_category()}"
            )
            category.deposit(
                amount=amount, description=f"Transfer from {self.get_category()}"
            )
            return True
        return False

    def __str__(self):
        shopping_lst = [
            f"{each_item['description'][:23]:<{23}}{each_item['amount']:>7.2f}"
            for each_item in self.get_ledger()
        ]
        shopping_lst.append(f"Total: {self.get_balance()}")
        formatted_spending_lst = "\n".join(shopping_lst)
        return f"{self.get_category().center(30, '*')}\n{formatted_spending_lst}"


def create_spend_chart(categories):
    bar_chart = ""

    def filter_withdraw_only(ledger_entries):
        return abs(sum([x["amount"] if x["amount"] < 0 else 0 for x in ledger_entries]))

    spend_in_category = [
        (category.get_category(), filter_withdraw_only(category.get_ledger()))
        for category in categories
    ]
    total_spend = sum([each[1] for each in spend_in_category])
    spend_percent_category = [
        {spend[0]: "o" * int(int(round((spend[1] / total_spend) * 100, -1)) / 10)}
        for spend in spend_in_category
    ]

    percent_ranges = "\n".join(
        list(map(lambda x: f"{x:>3}|", list(range(100, -10, -10))))
    )
    chart_txt = "Percentage spent by category\n"

    ex_str = []
    ex_str.append(percent_ranges)
    for each in spend_percent_category:
        val = list(each.values())[0]
        ex_str.append("\n" * (11 - len(val)) + "\n".join(val))
    split_lines = [each_line_str.split("\n") for each_line_str in ex_str]
    arranged_problems = "\n".join(
        " ".join(line) for line in zip_longest(*split_lines, fillvalue="")
    )

    hor_bar = " " * 4 + f"{((len(spend_percent_category)*2)+2)*'-'}"

    # shifted_bar = f"{hor_bar:>10}"
    bar_chart = chart_txt + arranged_problems + "\n" + hor_bar
    print(bar_chart)
