import logging


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Disable child views whose models are initialized later in the graph."""
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
                   AND data.module IN ('stock_voucher', 'l10n_ar_stock_ux')
           )
        """
    )
    _logger.info("Disabled %s stock child views loaded later", cr.rowcount)
