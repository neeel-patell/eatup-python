from django.db.models import *
from recipe.models import *
from user.models import *

class Expense(Model):
    schedule = ForeignKey(RecipeSchedule, on_delete=RESTRICT)
    amount = DecimalField(max_digits=6, decimal_places=2, null=False)
    user = ForeignKey(User, on_delete=RESTRICT)
    created_at = DateTimeField(auto_now=True)

    class Meta:
        db_table = "expense"

    def __str__(self):
        return "{} - {}".format(self.schedule.date, self.schedule.recipe.name)

class ExpenseUser(Model):
    expense = ForeignKey(Expense, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=RESTRICT)

    class Meta:
        db_table = "expense_user"

    def __str__(self):
        return "{} - {} - {}".format(self.expense.schdule.date, self.expense.schdule.recipe.name, self.user.name)