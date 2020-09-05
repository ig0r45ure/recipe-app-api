from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user with password as a username"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class OrgUnit(models.Model):
    """Organizational Unit who is owner of processes or does activities"""
    ORG_UNIT_CATEGORY = [
            (False, 'Terenowa Jednostka Organizacyjna'),
            (True, 'Komórka Organizacyjna Centrali'),
    ]

    name = models.CharField(max_length=255)
    acronym = models.CharField(max_length=16, blank=True, default='')
    is_HQUnit = models.BooleanField(
        choices=ORG_UNIT_CATEGORY,
        default=False,
    )

    def __str__(self):
        if self.acronym == '':
            return self.name
        else:
            return '%s - %s' % (self.name, self.acronym)


class Process(models.Model):
    """Business process - element of management architecture"""

    PROCESS_TYPE = [
            ('Operacyjny', 'Operacyjny'),
            ('Zarządzania', 'Zarządzania'),
            ('Wsparcia', 'Wsparcia'),
    ]

    PROCESS_LEVEL = [
            (True, 'poziom 1 (megaproces)'),
            (False, 'poziom 2 (proces)'),
    ]

    name = models.CharField(max_length=255)
    proc_id = models.CharField(max_length=4)
    is_megaprocess = models.BooleanField(
        default=False,
        choices=PROCESS_LEVEL)
    type = models.CharField(
        max_length=15,
        choices=PROCESS_TYPE,
    )
    owner = models.ForeignKey(
        'OrgUnit',
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'is_megaprocess': True}
    )

    def __str__(self):
        return '%s %s' % (self.proc_id, self.name)


class Procedure(models.Model):
    process = models.OneToOneField(
        'Process',
        on_delete=models.CASCADE,
        limit_choices_to={'is_megaprocess': False},
        unique_for_date='effective_date',
    )
    version = models.CharField(max_length=5, blank=True)
    developed_by = models.ForeignKey(
        'OrgUnit',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    effective_date = models.DateField()
    goal = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return 'Procedura do procesu %s' % (self.process)

class ProcedureInline(admin.TabularInline):
    model = Procedure


class Stakeholder(models.Model):
    """Stakeholder that participates in business processes"""
    STAKEHOLDER_TYPE = [
        (False,'zewnętrzny'),
        (True, 'wewnętrzny')
    ]

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.BooleanField(
        default=False,
        choices=STAKEHOLDER_TYPE
    )

    def __str__(self):
        return self.name


class WorkTask(models.Model):
    """WorkTask is a part of a action that has defined
        performers, participants and applications"""
    action = models.ForeignKey(
        'Action',
        on_delete=models.CASCADE,
    )
    in_action_order = models.PositiveSmallIntegerField()
    task = models.TextField()
    participants = models.CharField(max_length=255, blank=True)
    executive_units = models.ManyToManyField(
        'OrgUnit',
        related_name='responsible',
    )
    cooperative_units = models.ManyToManyField(
        'OrgUnit',
        related_name='cooperating'
    )
    stakeholders = models.ManyToManyField(
        'Stakeholder',
    )
    applications = models.CharField(max_length=255, blank=True)
    business_apps = models.ManyToManyField(
        'BusinessApp',
    )

    def __str__(self):
        return '%s %s %s' % (
            self.in_action_order,
            self.executive_unit,
            self.task,
        )


class WorkTaskInline(admin.TabularInline):
    model = WorkTask


class Action(models.Model):
    """Action is a part of a procedure for process that has defined
        input, products, performers and applications"""
    procedure = models.ForeignKey(
        'Procedure',
        on_delete=models.CASCADE,
    )
    in_process_step = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    trigger = models.CharField(max_length=255, blank=True)
    effects = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '%s: L.p. %s. %s' % (
            self.procedure,
            self.in_process_step,
            self.name
        )


class ActionInline(admin.TabularInline):
    model = Action


class BCMActivity(models.Model):
    """BCM Activity is a part of a process that is subject to BIA"""

    MTPD_TIMES = [
            (1, '4 godz.'),
            (2, 'dzień'),
            (3, '2 dni'),
            (4, 'tydzień'),
            (5, '2 tygodnie'),
            (6, 'miesiąc'),
            (7, '2 miesiące'),
            (8, 'do odwołania'),
    ]

    name = models.CharField(max_length=512)
    process = models.ForeignKey(
        'Process',
        on_delete=models.CASCADE,
        limit_choices_to={'is_megaprocess': False}
    )
    performer = models.ForeignKey(
        'OrgUnit',
        on_delete=models.CASCADE,
    )
    id_BIA = models.CharField(max_length=15, blank=True)
    MTPD = models.PositiveSmallIntegerField(
        choices=MTPD_TIMES
    )
    min_recovery_level = models.TextField(blank=True)
    TTN = models.PositiveSmallIntegerField(
        choices=MTPD_TIMES,
        blank=True,
    )

    def __str__(self):
        return '%s: [%s] %s' % (
            self.process,
            self.performer.acronym,
            self.name
        )


class BusinessApp(models.Model):
    """Software application that supports business processes"""

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
