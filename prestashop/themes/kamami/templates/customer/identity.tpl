{extends 'customer/page.tpl'}

{block name='page_title'}
  {l s='Twoje dane osobiste' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_header_container'}
  <header class="page-header">
    <h1>{l s='Twoje dane osobiste' d='Shop.Theme.Customeraccount'}</h1>
  </header>
{/block}

{block name='page_content'}
  {render file='customer/_partials/customer-form.tpl' ui=$customer_form}
{/block}

{block name='page_footer'}
  <footer class="page-footer">
    <a href="{$urls.pages.my_account}" class="account-link btn btn-primary">
      <i class="material-icons keyboard_arrow_left">&#xE314;</i>
      <span>{l s='Powrót do twojego konta' d='Shop.Theme.Actions'}</span>
    </a>
    <a href="{$urls.pages.index}" class="account-link btn btn-primary">
      <i class="material-icons home">&#xE88A;</i>
      <span>{l s='Strona główna' d='Shop.Theme.Global'}</span>
    </a>
  </footer>
{/block}