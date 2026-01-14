{**
 * Kamami theme footer template
 * Cloned from kamami.pl footer structure
 *}

{* Manufacturer carousel section *}
{block name='footer_before'}
  <div class="footer_before">
    <div class="container">
      <div class="row">
        {hook h='displayFooterBefore'}
      </div>
    </div>
  </div>
{/block}

{* Main footer container *}
<div class="footer-container">
  {* Go to top button *}
  <a href="#" id="go_top" title="{l s='Back to top' d='Shop.Theme.Actions'}">
    <i class="material-icons">keyboard_arrow_up</i>
  </a>

  <div class="container">
    <div class="row">
      {block name='hook_footer'}
        {hook h='displayFooter'}
      {/block}
    </div>

    {block name='hook_footer_after'}
      <div class="row">
        {hook h='displayFooterAfter'}
      </div>
    {/block}

    {* Copyright section *}
    <div class="row">
      <div class="col-md-12 copyright">
        <div class="text-sm-left bottom-footer">
          {block name='copyright_link'}
            <div>
              © {'Y'|date} - {$shop.name}
            </div>
          {/block}
        </div>
      </div>
    </div>
  </div>
</div>