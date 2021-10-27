{
    # debug
    http_port <EXPOSED_PORT>
    auto_https disable_redirects
}

:<EXPOSED_PORT>/static* {
    uri strip_prefix /static
    rewrite /static/ /

    file_server
    root * <DQAPP>/static_root
}

:<EXPOSED_PORT>/docs* {
    uri strip_prefix /docs
    reverse_proxy * <CONTAINER_DOCS>:8080
}

:<EXPOSED_PORT> {
    reverse_proxy * :8000
}
