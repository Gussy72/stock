import logging


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Disable views left by obsolete stock compatibility modules."""
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
                   AND data.module IN ('stock_voucher', 'l10n_ar_stock_adhoc')
           )
        """
    )
    _logger.info("Disabled %s obsolete stock compatibility views", cr.rowcount)
