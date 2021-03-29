{
    debug
    http_port <EXPOSED_PORT>
    auto_https disable_redirects
}

:<EXPOSED_PORT> {
    reverse_proxy * :8000
}

:<EXPOSED_PORT>/static* {
    uri strip_prefix /static
    rewrite /static/ /

    file_server
    root * <DQAPP>/static_root
}

:<EXPOSED_PORT>/cms* {

    redir /cms /cms/
    redir /cms/admin /cms/wp-admin/
    redir /cms/admin/ /cms/wp-admin/
    redir /cms/wp-admin /cms/wp-admin/

    uri strip_prefix /cms

    file_server
    root * <WORDPRESS_PATH>

    # socket for production, port for debug
    php_fastcgi unix//run/php/php.sock
    # php_fastcgi 127.0.0.1:9000
}
