import logging


_logger = logging.getLogger(__name__)


OBSOLETE_COMPATIBILITY_MODULES = (
    "account_tax_settlement",
    "l10n_ar_account_tax_settlement",
    "l10n_ar_account_withholding",
    "l10n_ar_stock_adhoc",
    "l10n_ar_withholding_ux",
    "stock_voucher",
)


def migrate(cr, version):
    """Disable every view left by modules replaced with compatibility shims."""
    cr.execute(
        """
        UPDATE ir_ui_view AS view
           SET active = FALSE
         WHERE view.active
           AND EXISTS (
                SELECT 1
                  FROM ir_model_data AS data
                 WHERE data.model = 'ir.ui.view'
                   AND data.res_id = view.id
                   AND data.module IN %s
           )
        """,
        [OBSOLETE_COMPATIBILITY_MODULES],
    )
    _logger.info(
        "Disabled %s views from obsolete compatibility modules", cr.rowcount
    )
