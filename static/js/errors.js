
function errorMessage(jqxhr,textStatus,response){
    console.log('error file',jqxhr)
    
        console.log('error file',response)
        var jsonarr = JSON.parse(JSON.stringify(response));
        
        var status = jsonarr.responseJSON.errors;
        if(status.length>1){
          toastr.error(status);
        }else{
        console.log(status);
        var main_error = [];
        for (var key in status) {
            console.log("Key: " + key);
            console.log("Value: " + status[key]);
            let str = `${status[key]}`;
            let strs = `${key}`
            if(strs != 'errors'){
              error = str.replace("This", strs);
            }else{
              error = str
            }
           
            main_error.push(error)
          }
    
          if(main_error[0] == 'Invalid pk "0" - object does not exist.'){
            toastr.error('Found Invalid Data');
          }else{
            toastr.error(main_error[0]);
          }
    }
    }