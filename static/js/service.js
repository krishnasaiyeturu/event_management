function getFormData(data) {
    var unindexed_array = data;
    var indexed_array = {};

    $.map(unindexed_array, function(n, i) {
      indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function EventTypeDropDown(id){
    return new Promise((resolve,reject) =>{
      
  
      $.ajax({
        type: "GET",
        url: "/api/event_type/",
        success: function (response,textStatus,xhr)
        {          
            let useroles = JSON.parse(JSON.stringify(response));
          if(xhr.status === 200)
          {
            var roleContent = `<option value="">Select Event Type</option>`;
            
           
            for (i = 0; i < useroles.length; i++)
            {
             if(useroles[i].id == "" || useroles[i].id == null  ){
               Event_ID = "Empty";
             }else{
              Event_ID = useroles[i].id;
            }
            if(useroles[i].name == "" || useroles[i].name == null  ){
              Name = "No Results ";
            } else{
              Name = useroles[i].name;
            }
            roleContent +='<option value="'+Event_ID+'">'+Name+'</option>';
            
          }
          $(`#${id}`).html(roleContent);    
          return resolve(true)                            
        }
      }
    });
  } )
  }



  function VenueDropDown(id){
    return new Promise((resolve,reject) =>{
      
  
      $.ajax({
        type: "GET",
        url: `/api/venue/`,
        success: function (response,textStatus,xhr)
        {          
            let useroles = JSON.parse(JSON.stringify(response));
          if(xhr.status === 200)
          {
            var roleContent = `<option value="">Select Venue</option>`;
            
           
            for (i = 0; i < useroles.length; i++)
            {
             if(useroles[i].id == "" || useroles[i].id == null  ){
                Venue_ID = "Empty";
             }else{
                Venue_ID = useroles[i].id;
            }
            if(useroles[i].name == "" || useroles[i].name == null  ){
              Name = "No Results ";
            } else{
              Name = useroles[i].name;
            }
            roleContent +='<option value="'+Venue_ID+'">'+Name+'</option>';
            
          }
          $(`#${id}`).html(roleContent);    
          return resolve(true)                            
        }
      }
    });
  } )
  }


  function PeopleDropDown(id,event_type,venue){
    return new Promise((resolve,reject) =>{
      
  
      $.ajax({
        type: "GET",
        url: `/api/price/?event_type=${event_type}&venue=${venue}`,
        success: function (response,textStatus,xhr)
        {          
            let useroles = JSON.parse(JSON.stringify(response));
          if(xhr.status === 200)
          {
            var roleContent = `<option value="">Select No of People</option>`;
            
           
            for (i = 0; i < useroles.length; i++)
            {
             if(useroles[i].id == "" || useroles[i].id == null  ){
                Venue_ID = "Empty";
             }else{
                Venue_ID = useroles[i].id;
            }
            if(useroles[i].no_of_participants == "" || useroles[i].no_of_participants == null  ){
              Name = "No Results ";
            } else{
              Name = "< " + useroles[i].no_of_participants;
            }
            roleContent +='<option value="'+Venue_ID+'">'+Name+'</option>';
            
          }
        //   $(`#${value_id}`).val(useroles[i].no_of_participants)
          $(`#${id}`).html(roleContent);    
          return resolve(true)                            
        }
      }
    });
  } )
  }