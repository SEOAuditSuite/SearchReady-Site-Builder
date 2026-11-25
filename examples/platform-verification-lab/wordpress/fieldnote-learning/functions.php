<?php
if (!defined('ABSPATH')) { exit; }
function fieldnote_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('automatic-feed-links');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script'));
    register_nav_menus(array('primary' => __('Primary navigation', 'fieldnote-learning')));
}
add_action('after_setup_theme', 'fieldnote_setup');
function fieldnote_assets() {
    wp_enqueue_style('fieldnote-style', get_stylesheet_uri(), array(), wp_get_theme()->get('Version'));
}
add_action('wp_enqueue_scripts', 'fieldnote_assets');
// Metadata, canonicals, robots and sitemaps remain owned by WordPress / the approved SEO plugin.
