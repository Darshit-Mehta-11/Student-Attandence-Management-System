from django.db import models
from accounts.models import CustomUser

class Result(models.Model):
    student = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    sem = models.IntegerField()
    ac_year = models.CharField(max_length=10)

    seo = models.IntegerField()
    c_sharp = models.IntegerField()
    php = models.IntegerField()
    python = models.IntegerField()
    java = models.IntegerField()


    def total_marks(self):
        return self.seo + self.c_sharp + self.php + self.python + self.java
    
    def percentage(self):
        return (self.seo + self.c_sharp + self.php + self.python + self.java) / 5

    
    def get_summary(self):
        sub=[self.seo,self.c_sharp,self.php,self.python,self.java]
        sub_fail=[]
        no_of_fail=0
        for i in sub:
            if i < 33:
                no_of_fail+=1

        if self.seo < 33:
            sub_fail.append("seo")
        
        data={
            "total_marks":self.seo + self.c_sharp + self.php + self.python + self.java,
            "percentage":(self.seo + self.c_sharp + self.php + self.python + self.java) / 5,
            "fail_count":no_of_fail,
            "fail_subject": sub_fail
        }
        return data

    def __str__(self):
        return self.student.username
    
    def no_of_subject(self):
        return [0,1,2,3,4]

    def pass_or_fail(self):
        fail_count={}
        if self.seo < 33:
            fail_count[0]="seo"
        if self.c_sharp < 33:
            fail_count[1]="c#"
        if self.php < 33:
            fail_count[2]="php"
        if self.python < 33:
            fail_count[3]="python"
        if self.java < 33:
            fail_count[4]="java"
        fail_count["total"]=len(fail_count)
        
        return fail_count
    
class find_sem():
    def __init__(self, sem):
        self.sem = sem

    def get_semester(self):
        if self.sem == 1:
            return "First Semester"
        elif self.sem == 2:
            return "Second Semester"
        elif self.sem == 3:
            return "Third Semester" 
        elif self.sem == 4:
            return "Fourth Semester"


class Fee(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    semester = models.PositiveSmallIntegerField(
        choices=[(1,'1st'),(2,'2nd'),(3,'3rd'),(4,'4th')],
        default=1
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - sem {self.semester} - {self.amount}"
