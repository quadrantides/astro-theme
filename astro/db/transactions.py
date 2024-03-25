from pytsprf.models import create_db_user
import transaction


def task_create_db_user(
        session,
        username,
        allowed_domain,
        allow_sub_domains=False
):

    with transaction.manager:

        creation, user = create_db_user(
            session,
            username,
            allowed_domain,
            allow_sub_domains=allow_sub_domains

        )

        transaction.commit()

    return creation, user
