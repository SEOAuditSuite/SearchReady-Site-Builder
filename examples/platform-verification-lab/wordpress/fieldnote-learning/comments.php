<?php if (post_password_required()) { return; } ?>
<section aria-label="<?php esc_attr_e('Comments', 'fieldnote-learning'); ?>"><?php if (have_comments()) { ?><h2><?php esc_html_e('Discussion', 'fieldnote-learning'); ?></h2><ol><?php wp_list_comments(); ?></ol><?php the_comments_pagination(); } comment_form(); ?></section>
