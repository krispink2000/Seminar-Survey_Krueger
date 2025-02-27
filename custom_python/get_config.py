from custom_python.general_helpers import make_field, get_raw


#####################
#### StartApp ####
#####################

### Preparation ###
path = "StartApp/config/json/preparation.json"

prep_gender_lb, prep_gender_ch = make_field(path, "gender", choices=True)

# adding * to the label of this field because its mandatory
prep_gender_lb = prep_gender_lb + "*"

prep_age_lb = make_field(path, "age") + "*"

prep_eligible_lb, prep_eligible_ch = make_field(path, "eligible", choices=True)

prep_eligible_lb = prep_eligible_lb + "*"

prep_participation_lb, prep_participation_ch = make_field(
    path, "participation", choices=True
)

prep_federal_state_lb, prep_federal_state_ch = make_field(
    path, "federal_state", choices=True
)

### Age Groups ###

path = "StartApp/config/json/age_groups.json"
age_groups = get_raw(path)["age_groups"]


### Quotas ###

path = "StartApp/config/json/quotas.json"
quotas = get_raw(path)["quotas"]
quotas_gender = quotas["gender"]
quotas_age = quotas["age"]
quotas_fs = quotas["federal_state"]

### Screen Outs ###

path = "StartApp/config/json/screen_outs.json"
screen_outs = get_raw(path)["screen_outs"]
screen_out_age = screen_outs["age"]
screen_out_eligible = screen_outs["eligible"]

###################
#### EndApp ####
###################


### Education ###
path = "EndApp/config/json/education.json"

edu_general_education_lb, edu_general_education_ch = make_field(
    path, "general_education", choices=True
)

edu_vocational_training_lb, edu_vocational_training_ch = make_field(
    path, "vocational_training", choices=True
)

### Income ###

path = "EndApp/config/json/income.json"

income_net_income_lb, income_net_income_ch = make_field(
    path, "net_income", choices=True
)
