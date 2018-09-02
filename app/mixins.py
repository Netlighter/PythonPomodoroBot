from users.schemas import User


class UpdateUserStateMixin:
    """
    Mixin for updating user's state (returned by callback) in mongo db.
    """
    # Spefical state which means 'do not change user state in db'.
    KEEP_CURRENT_STATE = 'KEEP_CURRENT_STATE'

    def post_callback_procession(self, state):
        if state != self.KEEP_CURRENT_STATE:
            user_obj = User.objects.get(telegram_id=self.user.id)
            user_obj.state = state
            user_obj.save()

        return super().post_callback_procession(state)


class RequiredStateMixin:
    """
    Mixin which requires user to have concrete state for handler to be matched.
    """
    REQUIRED_STATE = NotImplemented

    def __init__(self, *args, **kwargs):
        if self.REQUIRED_STATE is NotImplemented:
            raise NotImplementedError(
                'Using RequiredStateMixin you must implement REQUIRED_STATE '
                'class attribute!')

        super().__init__(*args, **kwargs)

    def check_update(self, update):
        pattern_matched = super().check_update(update)

        user_has_correct_state = (
            User.objects.get(telegram_id=self.user.id).state
            == self.REQUIRED_STATE)

        return pattern_matched and user_has_correct_state
