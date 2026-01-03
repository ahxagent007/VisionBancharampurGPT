from django.db import transaction
from django.utils import timezone
from ledger.services import add_ledger_entry

@transaction.atomic
def create_asset_with_ledger(*, asset_obj, created_by):
    """
    Call after saving Asset to create ledger OUT entry.
    """
    add_ledger_entry(
        date=asset_obj.purchase_date or timezone.now().date(),
        entry_type="ASSET_PURCHASE",
        direction="OUT",
        amount=asset_obj.purchase_cost,
        created_by=created_by,
        member=None,
        description=f"Asset purchase: {asset_obj.title} (Project: {asset_obj.project.name})",
    )
