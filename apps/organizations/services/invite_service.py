from django.db import transaction
from ..models import Organization, Membership, Invite
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteService:
    
    @staticmethod
    @transaction.atomic
    def send_invites(*, organization, inviter, invitee_email=None, invitee_id=None, role=Membership.Role.STAFF):

        if not inviter.memberships.filter(organization=organization, role=Membership.Role.ADMIN).exists():
            raise PermissionError("Only ADMIN can send invite")
        
        user_to_invite = None
        if invitee_id:
            user_to_invite = User.objects.filter(id=invitee_id).first()
        elif invitee_email:
            user_to_invite = User.objects.filter(email=invitee_email).first() 

        if not user_to_invite:
            raise ValueError("User must be registered to receive an invite.")

        if organization.memberships.filter(user=user_to_invite).exists():
            raise ValueError("User is already a member of this organization.")
                
        if Invite.objects.filter(organization=organization, invitee=user_to_invite , status='PENDING').exists():
            raise ValueError("An invitation is already pending for this user.")

        return Invite.objects.create(
            organization=organization,
            invitee=user_to_invite,
            email=user_to_invite.email,
            invited_by=inviter,
            role=role
        )            


    @staticmethod
    @transaction.atomic
    def cancel_invite(*, invite, cancelled_by):
        """
        Logic: Only the original inviter OR the Org Admin can cancel a pending invite.
        """
        is_inviter = invite.invited_by == cancelled_by
        
        if not is_inviter:
            is_admin = invite.organization.memberships.filter(
                user=cancelled_by, 
                role=Membership.Role.ADMIN
            ).exists()
            
            if not is_admin:
                raise PermissionError("Only the inviter or an admin can cancel this invite.")

        # State check
        if invite.status != Invite.Status.PENDING:
            raise ValueError(f"Cannot cancel an invite that is already {invite.status.lower()}.")

        invite.status = Invite.Status.CANCELLED            
        invite.save(update_fields=["status"])

    @staticmethod
    @transaction.atomic
    def accept_invite(*, user, invite):
        """
        Accepts an invitation and joins the organization.
        """
        if invite.invitee != user or invite.email.lower() != user.email.lower():
            raise PermissionError("This invitation was not issued to your account.")            

        if invite.status != Invite.Status.PENDING:
            raise ValueError("This invitation is no longer valid.")

        if Membership.objects.filter(user=user, organization=invite.organization).exists():
            raise ValueError("You are already a member of this organization.")
            
        membership = Membership.objects.create(
        user=user,
        organization=invite.organization,
        role=invite.role
    )    

        invite.status = Invite.Status.ACCEPTED
        invite.save(update_fields=["status"])

        return membership
    

    @staticmethod
    @transaction.atomic
    def reject_invite(*, user, invite):
        if invite.invitee != user or invite.email.lower() != user.email.lower():
            raise PermissionError("This invitation was not issued to your account.")

        if invite.status != Invite.Status.PENDING:
            raise ValueError(f"This invite is already {invite.status.lower()}")    

        invite.status = Invite.Status.REJECTED
        invite.save(update_fields=["status"])