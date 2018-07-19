/**
 * Created by ne_luboff on 19.07.18.
 */

//$(document).ready ( function(){
window.onload = ( function(){
    var password = "qwerty";
    var randomSeed = lightwallet.keystore.generateRandomSeed();

    lightwallet.keystore.createVault({password: password, seedPhrase: randomSeed, hdPathString: "m/44'/60'/0'/0"}, function (err, ks) {
        ks.keyFromPassword(password, function(err, pwDerivedKey) {
            ks.generateNewAddress(pwDerivedKey);

            var address = ks.getAddresses();
            var key = ks.exportPrivateKey(address[0], pwDerivedKey);

			var data = JSON.stringify({address:address[0],seed:randomSeed,privateKey:key,password:password}, null, 2);
            console.log(data);
            document.write( "<pre>" + data + "</pre>") ;
        })
    })
});