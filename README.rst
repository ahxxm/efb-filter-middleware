A filter middleware for EFB
==============
A filter middleware for EFB to help block messages from unwanted WeChat senders.

Install
-----------------
install using pip::
    
    pip install -U git+https://github.com/ahxxm/efb-filter-middleware

Configuration
-----------------
append middleware id ``ahxxm.filter`` to ``~/.ehforwarderbot/profiles/default/config.yaml``::

    master_channel: blueset.telegram
    slave_channels:
      - blueset.wechat
    middlewares:
      - ahxxm.filter

config file is located in ``~/.ehforwarderbot/profiles/default/ahxxm.filter/config.yaml``, a sample config file::

    block_names:
      - 招商银行
      - 中国电信营业厅

the middleware implemented hot reloading, updates to ``config.yaml`` will start to apply on next message arrival.
