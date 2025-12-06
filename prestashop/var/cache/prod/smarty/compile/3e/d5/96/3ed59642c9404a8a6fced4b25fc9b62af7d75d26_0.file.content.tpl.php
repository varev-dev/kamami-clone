<?php
/* Smarty version 3.1.48, created on 2025-12-06 02:46:26
  from '/var/www/html/admin-panel/themes/default/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_69338af21c4617_24148592',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '3ed59642c9404a8a6fced4b25fc9b62af7d75d26' => 
    array (
      0 => '/var/www/html/admin-panel/themes/default/template/content.tpl',
      1 => 1702485415,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_69338af21c4617_24148592 (Smarty_Internal_Template $_smarty_tpl) {
?><div id="ajax_confirmation" class="alert alert-success hide"></div>
<div id="ajaxBox" style="display:none"></div>

<div class="row">
	<div class="col-lg-12">
		<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
			<?php echo $_smarty_tpl->tpl_vars['content']->value;?>

		<?php }?>
	</div>
</div>
<?php }
}
