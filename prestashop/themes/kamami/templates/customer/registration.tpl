{extends file='page.tpl'}

{block name='page_title'}
  {l s='Stwórz konto' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_header_container'}
  <header class="page-header">
    {block name='page_title'}
      <h1 class="page-title">{l s='Stwórz konto' d='Shop.Theme.Customeraccount'}</h1>
    {/block}
  </header>
{/block}

{block name='page_content'}
  {block name='register_form_container'}
    <div class="card card-login">
      <div class="card-body">
        <section class="register-form">
          <p>{l s='Masz już konto?' d='Shop.Theme.Customeraccount'} <a
              href="{$urls.pages.authentication}">{l s='Zaloguj się!' d='Shop.Theme.Customeraccount'}</a></p>

          {render file='customer/_partials/customer-form.tpl' ui=$register_form}
        </section>
      </div>
    </div>
  {/block}
{/block}

{block name='page_footer'}
  <footer class="page-footer">
    <a href="{$urls.pages.my_account}" class="account-link">
      <i class="material-icons keyboard_arrow_left">&#xE314;</i>&nbsp;
      <span>{l s='Powrót do logowania' d='Shop.Theme.Actions'}</span>
    </a>
  </footer>
{/block}