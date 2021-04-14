<?php

// ** MySQL settings - You can get this info from your web host ** //
define('DB_NAME', '<WORDPRESS_DB_NAME>');
define('DB_USER', '<WORDPRESS_DB_USER>');
define('DB_PASSWORD', '<WORDPRESS_DB_PASSWORD>');
define('DB_HOST', '<WORDPRESS_DB_HOST>');
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

$table_prefix  = 'wp_';
define('WP_DEBUG', true);
define('SCRIPT_DEBUG', true );

if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
    $_SERVER['HTTP_HOST'] = '<URL_HOSTNAME>';
    $_SERVER['SERVER_NAME'] = '<URL_HOSTNAME>';
}

define('CONCATENATE_SCRIPTS', false);
define('DAIQUIRI_DEBUG', True);

define('COOKIEPATH', '/');
define('SITECOOKIEPATH', COOKIEPATH);
define('ADMIN_COOKIE_PATH', COOKIEPATH);
define('PLUGINS_COOKIE_PATH', COOKIEPATH);

define('WP_HOME', '<URL_PROTOCOL>://<URL_HOSTNAME>/cms' );
define('WP_SITEURL', '<URL_PROTOCOL>://<URL_HOSTNAME>/cms');
define('DAIQUIRI_URL', '<URL_PROTOCOL>://<URL_HOSTNAME>');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'put your unique phrase here');
define('SECURE_AUTH_KEY',  'put your unique phrase here');
define('LOGGED_IN_KEY',    'put your unique phrase here');
define('NONCE_KEY',        'put your unique phrase here');
define('AUTH_SALT',        'put your unique phrase here');
define('SECURE_AUTH_SALT', 'put your unique phrase here');
define('LOGGED_IN_SALT',   'put your unique phrase here');
define('NONCE_SALT',       'put your unique phrase here');
/**#@-*/

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

?>
