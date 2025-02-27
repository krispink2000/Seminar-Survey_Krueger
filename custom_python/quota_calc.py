from custom_python.general_helpers import calc_byear
import custom_python.get_config as cf


def counting(player):
    # COUNTING UP THE QUOTAS
    if player.participant.screen_out == 0 and player.participant.quota == 0:
        # GENDER
        if player.participant.gender != -999:
            player.session.vars[
                f"completed_gender_{player.participant.gender}"
            ] += 1
        # AGE
        player.session.vars[
            f"completed_age_group_{player.participant.age_group}"
        ] += 1

        # FEDERAL STATE
        if player.participant.screen_out not in [None, -888]:
            player.session.vars[
                f"completed_federal_state_{player.participant.federal_state}"
            ] += 1


def filtering(player):
    # QUOTA
    player.participant.quota = False

    ## GENDER
    if player.field_maybe_none("prep_gender") != -999:
        gender = player.prep_gender
        value = player.session.vars[f"completed_gender_{gender}"]
        if value >= cf.quotas_gender[gender]:
            player.participant.quota = True

    ## AGE GROUPS
    grp = [
        i
        for (i, [lwr, upr]) in enumerate(cf.age_groups)
        if calc_byear(lwr) >= player.prep_age >= calc_byear(upr)
    ]
    if len(grp) == 1:
        player.participant.age_group = grp[0]
        complete_cases = player.session.vars[f"completed_age_group_{grp[0]}"]
        if complete_cases >= cf.quotas_age[grp[0]]:
            player.participant.quota = True
    elif len(grp) > 1:
        raise Exception(
            "Participant in more than one age group. Groups must not overlap."
        )

    ## FEDERAL STATES
    unknown_state = player.field_maybe_none("prep_federal_state") in [
        None,
        -888,
    ]
    if not unknown_state:
        fs = player.prep_federal_state
        complete_cases = player.session.vars[f"completed_federal_state_{fs}"]
        if complete_cases >= cf.quotas_fs[fs]:
            player.participant.quota = True

    # SCREENOUTS
    ineligible = player.prep_eligible != 0 and cf.screen_out_eligible
    player.participant.screen_out = len(grp) != 1 or ineligible or unknown_state
