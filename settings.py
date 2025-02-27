from os import environ
import custom_python.get_config as cf
import os 
import warnings 

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
    normal_redirect_link="https://mingle.respondi.com/s/1608318/ospe.php3?c_0002=1&return_tic=",
    screen_out_redirect_link="https://survey.maximiles.com/screenout?p=89808_546de779&m=",
    quota_redirect_link="https://survey.maximiles.com/quotasfull?p=89808_d7bfcc1a&m=",
    quota_screenout=True,
)

SESSION_CONFIGS = [
    dict(
        name='seminar_survey',
        display_name='Seminar Survey',
        num_demo_participants=10,
        app_sequence=["StartApp", 
                      "SocialmediaApp",
                      "MobilizationApp",
                      "CandidateApp", 
                      "EndApp"],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

PARTICIPANT_FIELDS = [
    "b_group",
    "federal_state",
    "eligible",
    "gender",
    "age_group",
    "quota",
    "screen_out",
]

SESSION_FIELDS = (
    list(
        map(
            lambda i: f"completed_gender_{i}", range(len(cf.prep_gender_ch) - 1)
        )
    )
    + list(map(lambda i: f"completed_age_group_{i}", range(len(cf.age_groups))))
    + list(
        map(
            lambda i: f"completed_federal_state_{i}",
            range(len(cf.prep_federal_state_ch) - 1),
        )
    )
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True


ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = os.environ.get("OTREE_ADMIN_PASSWORD")

OTREE_AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL', None)


match os.environ.get("OTREE_REST_KEY"):
    case "" | None:
        SECRET_KEY = "5903222485487"
        warnings.warn(
            "Environmental variable for REST key not set. Using default.",
            stacklevel=1,
        )
    case _:
        SECRET_KEY = os.environ.get("OTREE_REST_KEY")

# Database credentials
if (
    os.environ.get("POSTGRES_PASSWORD")
    and os.environ.get("POSTGRES_USER")
    and os.environ.get("POSTGRES_DB")
):
    os.environ["DATABASE_URL"] = (
        "postgres://"
        + os.environ.get("POSTGRES_USER")
        + ":"
        + os.environ.get("POSTGRES_PASSWORD")
        + "@db/"
        + os.environ.get("POSTGRES_DB")
    )
elif (
    os.environ.get("POSTGRES_PASSWORD")
    or os.environ.get("POSTGRES_USER")
    or os.environ.get("POSTGRES_DB")
):
    warnings.warn(
        """To use Postgres, the environmental variables DATABASE_URL,
        POSTGRES_USER, and POSTGRES_DB must all be set""",
        stacklevel=1,
    )
elif os.environ.get("DATABASE_URL"):
    pass
else:
    warnings.warn(
        """Using SQLite, because no Postgres credentials are specified. This is
        fine for local use, but can lead to performance degradation in
        production.""",
        stacklevel=1,
    )

