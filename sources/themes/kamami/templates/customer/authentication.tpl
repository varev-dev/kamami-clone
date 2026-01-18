{extends file='page.tpl'}

{block name='page_title'}
  {l s='Zaloguj się do swojego konta' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_header_container'}
  <header class="page-header">
    {block name='page_title'}
      <h1>{l s='Zaloguj się do swojego konta' d='Shop.Theme.Customeraccount'}</h1>
    {/block}
  </header>
{/block}

{block name='page_content'}
  {block name='login_form_container'}
    <section class="login-form">
      {render file='customer/_partials/login-form.tpl' ui=$login_form}
    </section>

    <div class="login-form-links" style="margin-top: 2rem;">
      <div class="no-account">
        <a href="{$urls.pages.register}" data-link-action="display-register-form">
          {l s='Nie masz konta? Załóż je tutaj' d='Shop.Theme.Customeraccount'}
        </a>
      </div>
      <div class="forgot-password">
        <a href="{$urls.pages.password}" rel="nofollow">
          {l s='Nie pamiętasz hasła?' d='Shop.Theme.Customeraccount'}
        </a>
      </div>
    </div>
  {/block}
{/block}

{block name='page_footer'}
  <footer class="page-footer">
    {* Footer content *}
  </footer>
{/block}