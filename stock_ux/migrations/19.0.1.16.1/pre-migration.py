import logging


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Disable legacy stock voucher views before validating stock move views."""
    cr.execute(
        """
        UPDATE ir_ui_view
           SET active = FALSE
         WHERE active
           AND arch_db::text LIKE '%%vouchers%%'
        """
    )
    _logger.info("Disabled %s legacy stock voucher views", cr.rowcount)
