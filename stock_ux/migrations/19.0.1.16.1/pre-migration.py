import logging


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Disable legacy stock voucher views before validating stock views."""
    cr.execute(
        """
        UPDATE ir_ui_view AS view
           SET active = FALSE
         WHERE view.active
           AND (
                view.arch_db::text ~ '(vouchers|book_id|voucher_required|book_required|voucher_number_unique|dispatch_number)'
                OR EXISTS (
                    SELECT 1
                      FROM ir_model_data AS data
                     WHERE data.model = 'ir.ui.view'
                       AND data.res_id = view.id
                       AND data.module IN ('stock_voucher', 'l10n_ar_stock_adhoc', 'l10n_ar_stock_ux')
                )
           )
        """
    )
    _logger.info("Disabled %s legacy stock voucher views", cr.rowcount)
