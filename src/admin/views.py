from sqladmin import ModelView
from sqlalchemy import event

from src.auth.auth import get_password_hash
from src.models import LeadContact, User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_list = [User.id, User.email]
    column_details_exclude_list = [User.hashed_password]
    can_delete = True

    @event.listens_for(User.hashed_password, 'set', retval=True)
    def hash_user_password(target, value, oldvalue, initiator):
        if value != oldvalue:
            return get_password_hash(value)
        return value


class LeadContactAdmin(ModelView, model=LeadContact):
    name = "Lead Contact"
    name_plural = "Lead Contacts"
    icon = "fa-solid fa-book"
    column_list = [
        LeadContact.id,
        LeadContact.lead_name,
        LeadContact.linkedin_profile,
        LeadContact.next_contact,
        LeadContact.status,
        LeadContact.created_at,
    ]
    column_searchable_list = [
        LeadContact.lead_name,
        LeadContact.linkedin_profile,
    ]
    column_sortable_list = [
        LeadContact.status,
        LeadContact.created_at,
    ]
