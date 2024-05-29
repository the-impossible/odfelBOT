from django.db import models

# Create your models here.
class Session(models.Model):
    session = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.session}'

    class Meta:
        db_table = 'Session'
        verbose_name_plural = 'Sessions'

class Department(models.Model):
    department = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.department}'

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Departments'

class Level(models.Model):
    level = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.level}'

    class Meta:
        db_table = 'Level'
        verbose_name_plural = 'Levels'

class Semester(models.Model):
    semester = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.semester}'

    class Meta:
        db_table = 'Semester'
        verbose_name_plural = 'Semesters'

class Course(models.Model):
    title = models.CharField(max_length=500)
    code = models.CharField(max_length=500)
    unit = models.IntegerField(default=2)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'Course'
        verbose_name_plural = 'Courses'

class Links(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    links = models.URLField(max_length=500)

    def __str__(self):
        return f'{self.level} | {self.course} | {self.links}'

    class Meta:
        db_table = 'Links'
        verbose_name_plural = 'Links'

class SessionLink(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    links = models.URLField(max_length=500)

    def __str__(self):
        return f'{self.session} session | {self.links}'

    class Meta:
        db_table = 'Session Link'
        verbose_name_plural = 'Session Link'

class Announcement(models.Model):
    title = models.CharField(max_length=500)
    desc = models.TextField(max_length=1000)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'Announcement'
        verbose_name_plural = 'Announcements'

class CourseRepresentative(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=14)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'CourseRepresentative'
        verbose_name_plural = 'CourseRepresentatives'
