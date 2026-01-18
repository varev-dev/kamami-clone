{extends file='checkout/_partials/steps/checkout-step.tpl'}

{block name='step_content'}
  {hook h='displayPersonalInformationTop' customer=$customer}

  {if $customer.is_logged && !$customer.is_guest}

    <p class="identity">
      {* [1][/1] is for a HTML tag. *}
      {l s='Connected as [1]%firstname% %lastname%[/1].'
            d='Shop.Theme.Customeraccount'
            sprintf=[
              '[1]' => "<a href='{$urls.pages.identity}'>",
      '[/1]' => "</a>",
      '%firstname%' => $customer.firstname,
      '%lastname%' => $customer.lastname
      ]
      }
    </p>
    <p>
      {* [1][/1] is for a HTML tag. *}
      {l
            s='Not you? [1]Log out[/1]'
            d='Shop.Theme.Customeraccount'
            sprintf=[
            '[1]' => "<a href='{$urls.actions.logout}'>",
      '[/1]' => "</a>"
      ]
      }
    </p>
    {if !isset($empty_cart_on_logout) || $empty_cart_on_logout}
      <p><small>{l s='If you sign out now, your cart will be emptied.' d='Shop.Theme.Checkout'}</small></p>
    {/if}

    <div class="clearfix">
      <form method="GET" action="{$urls.pages.order}">
        <button class="continue btn btn-primary float-xs-right" name="controller" type="submit" value="order">
          {l s='Continue' d='Shop.Theme.Actions'}
        </button>
      </form>

    </div>

  {else}
    <div class="personal-inf">
      <div class="personal-inf1" id="checkout-guest-form">
        <div class="personal-inf-login">
          <h3>Zaloguj się</h3>
          {render file='checkout/_partials/login-form.tpl' ui=$login_form}
        </div>
        <div class="personal-inf-create">
          <h3>Załóż konto i ciesz się wygodą zakupów!</h3>
          <div>
            <span class="create-acc-txt">
              Dołączając do grona zarejestrowanych użytkowników Kamami, zyskujesz dostęp do praktycznych funkcji i
              dodatkowych benefitów, które umilą Ci zakupy oraz korzystanie z naszego sklepu. Przekonaj się sam, dlaczego
              warto posiadać własne konto. Poniżej znajdziesz przykładowe zalety, które przygotowaliśmy specjalnie dla
              Ciebie:
            </span>
            <ul class="create-acc-list">
              <li class="create-acc-1">Możliwość szybszego składania zamówień</li>
              <li class="create-acc-2">Specjalne oferty i promocje</li>
              <li class="create-acc-3">Dostęp do historii zamówień</li>
            </ul>
            <span class="create-acc-txt">
              Aby utworzyć konto, wystarczy, że ustawisz hasło podczas składania zamówienia jako gość, a my automatycznie
              utworzymy Twoje konto!
            </span>
          </div>
        </div>
      </div>
      <div class="personal-inf2" id="checkout-login-form">
        <h3>Zamówienie jako gość</h3>
        {render file='checkout/_partials/customer-form.tpl' ui=$register_form guest_allowed=$guest_allowed}
      </div>
    </div>
  {/if}
{/block}