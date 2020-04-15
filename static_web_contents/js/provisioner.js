$(document).ready(function(){
    $("#confirm").click(function(){

        var infraPayload = {
            BucketName: 'test-waj-bucket-cft'
        }

        var body = {
            governance: 'ENABLED',
            option: 'VALIDATION',
            payload: 're',
            env: 'test-env'
        }

        fetch('https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/provisioner', {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        })
        .then(r => r.json())
        .then(d => {
            if (d.executionArn !== '') {
                console.log('Test: ' + d.executionArn);
                getExectutionStatus(
                    'https://qc6lo72n44.execute-api.eu-west-2.amazonaws.com/beta/execution',
                    JSON.stringify(d))
            }
        })
        .catch(err => { console.log(err) });
    });
});

function getExectutionStatus(url, arn) {
    fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {'Content-Type': 'application/json'},
        body: arn
    })
    .then(resp => resp.json())
    .then(d => { 
        console.log('HIIIITTTT');
        if (d.status === 'RUNNING') {
            getExectutionStatus(url, arn);
        } else {
            console.log(d);
        }
     })
    .catch(err => { console.log(err) })
}