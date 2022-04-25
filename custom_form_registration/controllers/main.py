from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.web.controllers import main

main.SIGN_UP_REQUEST_PARAMS |= {'mobile'}
CustomerPortal.MANDATORY_BILLING_FIELDS.append('mobile')


class AuthSignup(AuthSignupHome):

    def _prepare_signup_values(self, qcontext):
        values = super(AuthSignup, self)._prepare_signup_values(qcontext)
        values.update({'mobile': qcontext.get('mobile')})
        return values
