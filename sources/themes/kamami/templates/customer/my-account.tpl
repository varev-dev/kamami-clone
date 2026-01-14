{extends file='customer/page.tpl'}

{block name='page_title'}
  {l s='Twoje konto' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_content'}
  <div class="row">
    <div class="links">
      <style>
        .links>a,
        .links>li>a {
          width: 50% !important;
          max-width: 50% !important;
        }

        @media (max-width: 991px) {

          .links>a,
          .links>li>a {
            width: 100% !important;
            max-width: 100% !important;
          }
        }
      </style>

      <a class="col-lg-6 col-md-6 col-sm-6 col-xs-12" id="identity-link" href="{$urls.pages.identity}">
        <span class="link-item">
          <i class="material-icons">&#xE853;</i>
          {l s='Informacje' d='Shop.Theme.Customeraccount'}
        </span>
      </a>

      {if $customer.addresses|count}
        <a class="col-lg-6 col-md-6 col-sm-6 col-xs-12" id="addresses-link" href="{$urls.pages.addresses}">
          <span class="link-item">
            <i class="material-icons">&#xE56A;</i>
            {l s='Adresy' d='Shop.Theme.Customeraccount'}
          </span>
        </a>
      {else}
        <a class="col-lg-6 col-md-6 col-sm-6 col-xs-12" id="address-link" href="{$urls.pages.address}">
          <span class="link-item">
            <i class="material-icons">&#xE567;</i>
            {l s='Dodaj adres' d='Shop.Theme.Customeraccount'}
          </span>
        </a>
      {/if}

      {if !$configuration.is_catalog}
        <a class="col-lg-6 col-md-6 col-sm-6 col-xs-12" id="history-link" href="{$urls.pages.history}">
          <span class="link-item">
            <i class="material-icons">&#xE916;</i>
            {l s='Historia zamówień i szczegóły' d='Shop.Theme.Customeraccount'}
          </span>
        </a>
      {/if}

      {if !$configuration.is_catalog}
        <a class="col-lg-6 col-md-6 col-sm-6 col-xs-12" id="discounts-link" href="{$urls.pages.discount}">
          <span class="link-item">
            <i class="material-icons">&#xE54E;</i>
            {l s='Kupony' d='Shop.Theme.Customeraccount'}
          </span>
        </a>
      {/if}

      {block name='display_customer_account'}
        {* 
          {hook h='displayCustomerAccount'}
        *}
      {/block}

    </div>
  </div>
{/block}

{block name='page_footer'}
  <footer class="page-footer">
    <div class="container">
      <div class="text-sm-center">
        <a href="{$urls.actions.logout}" class="btn btn-primary">
          <i class="material-icons exit_to_app input">&#xE8B5;</i>
          {l s='Wyloguj się' d='Shop.Theme.Actions'}
        </a>
      </div>
    </div>
  </footer>
{/block}