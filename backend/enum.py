class AccountStatus:
    TRIAL = 'TRIAL'
    PREMIUM = 'PREMIUM'

    @staticmethod
    def get_choices():
        return (
            (AccountStatus.TRIAL, 'Trial'),
            (AccountStatus.PREMIUM, 'Premium'),
        )
