<?php get_header(); ?>
<main id="main" class="wrap">
<section class="hero"><p class="eyebrow"><?php esc_html_e('Learning resources', 'fieldnote-learning'); ?></p><h1><?php if (is_home()) { echo esc_html(get_bloginfo('name')); } else { the_archive_title(); } ?></h1><?php if (is_home()) { ?><p><?php echo esc_html(get_bloginfo('description')); ?></p><?php } else { the_archive_description(); } ?></section>
<?php if (have_posts()) { ?><div class="grid"><?php while (have_posts()) { the_post(); ?><article <?php post_class('card'); ?>><?php if (has_post_thumbnail()) { the_post_thumbnail('medium_large'); } ?><h2><a href="<?php echo esc_url(get_permalink()); ?>"><?php the_title(); ?></a></h2><?php the_excerpt(); ?></article><?php } ?></div><div class="pagination"><?php the_posts_pagination(); ?></div><?php } else { ?><p><?php esc_html_e('No resources are available yet.', 'fieldnote-learning'); ?></p><?php get_search_form(); } ?>
</main><?php get_footer(); ?>
