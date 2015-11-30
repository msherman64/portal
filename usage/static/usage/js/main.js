"use strict";angular.module("underscore",[]).factory("_",function(){return window._}),angular.module("moment",[]).factory("moment",function(){return window.moment}),angular.module("highcharts",[]).factory("highcharts",function(){return window.Highcharts}),angular.module("usageApp.service",[]),angular.module("usageApp",["underscore","moment","highcharts","usageApp.service","ui.bootstrap","highcharts-ng"]).config(["$interpolateProvider","$httpProvider",function(a,b){a.startSymbol("[[").endSymbol("]]"),b.defaults.headers.common["X-Requested-With"]="XMLHttpRequest",b.defaults.headers.post["Content-Type"]="application/x-www-form-urlencoded",b.defaults.xsrfCookieName="csrftoken",b.defaults.xsrfHeaderName="X-CSRFToken"}]);var app=angular.module("usageApp");app.directive("readMore",function(){return{restrict:"A",transclude:!0,replace:!0,template:"<p></p>",scope:{moreText:"@",lessText:"@",words:"@",ellipsis:"@","char":"@",limit:"@",content:"@",textData:"@"},link:function(a,b,c){function d(){var a=i,d=/\s+/gi,j=i.length,k=i.trim().replace(d," ").split(" ").length,l="char",m=j,n=[],o=i,p="";angular.isUndefined(c.words)||(l="words",m=k),"words"===l?(n=i.split(/\s+/),n.length>h&&(i=n.slice(0,h).join(" ")+g,p=n.slice(h,m).join(" "),o=i+e+'<span class="more-text">'+p+f+"</span>")):m>h&&(i=a.slice(0,h)+g,p=a.slice(h,m),o=i+e+'<span class="more-text">'+p+f+"</span>"),b.append(o),b.find(".more-text").hide().removeClass("show-inline"),b.find(".read-more").on("click",function(){$(this).hide(),b.find(".more-text").addClass("show-inline").slideDown()}),b.find(".read-less").on("click",function(){b.find(".read-more").show(),b.find(".more-text").hide().removeClass("show-inline")})}var e=angular.isUndefined(a.moreText)?' <a class="read-more">Read More...</a>':' <a class="read-more">'+a.moreText+"</a>",f=angular.isUndefined(a.lessText)?' <a class="read-less">Less ^</a>':' <a class="read-less">'+a.lessText+"</a>",g=angular.isUndefined(a.ellipsis)?"":a.ellipsis,h=angular.isUndefined(a.limit)?50:a.limit,i=angular.isUndefined(a.textData)?"":a.textData.trim();d()}}}),angular.module("usageApp.service").factory("NotificationFactory",["$rootScope","$timeout","_",function(a,b,c){var d={},e={},f={};return d.uuid=function(){return"xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,function(a){var b=16*Math.random()|0,c="x"===a?b:3&b|8;return c.toString(16)})},d.addLoading=function(b){f[b]=!0,a.$broadcast("allocation:notifyLoading")},d.removeLoading=function(b){delete f[b],a.$broadcast("allocation:notifyLoading")},d.getMessages=function(){return e},d.getLoading=function(){return f},d.clearMessages=function(b){b=b||"all","all"===b?e={}:e[b]=[],a.$broadcast("allocation:notifyMessage")},d.removeMessage=function(b,d,f){"undefined"!=typeof f&&(b+=f);var g=e[b];!g||g.length<1||(e[b]=c.reject(g,function(a){return a._id===d._id}),a.$broadcast("allocation:notifyMessage"))},d.addMessage=function(c,f,g){var h={};h.body=f,h.type=g,h._id=d.uuid(),"undefined"==typeof e[c]&&(e[c]=[]),e[c].push(h),a.$broadcast("allocation:notifyMessage");var i="danger"===h.type?0:5e3;i>0&&b(function(){d.removeMessage(c,h)},i)},d}]).factory("UtilFactory",["_","moment","NotificationFactory",function(a,b,c){var d={};return d.getClass=function(a){var b=a.status.toLowerCase();return"pending"===b?"label label-warning":"rejected"===b?"label label-danger":"label label-success"},d.isLoading=function(a,b){if(!a||!b)return!1;var d=a+b.id;return"undefined"==typeof c.getLoading()[d]?!1:!0},d.closeMessage=function(a,b,d){d="undefined"==typeof d||null===d?"":d,a+=d,c.removeMessage(a,b)},d.isEmpty=function(b){return"undefined"!=typeof b&&b?angular.isArray(b)&&0===b.length?!0:angular.isObject(b)&&a.isEmpty(b)?!0:!1:!0},d.hasMessage=function(a,b){var c=!1;if("undefined"==typeof a||null===a||a===[]||"undefined"==typeof b||null===b||""===b)return c;for(var d in a)if(a[d].type===b){c=!0;break}return c},d.getMessages=function(a,b){if(!a||!b)return[];var d=a+b.id,e=c.getMessages()[d];return"undefined"!=typeof e&&e.length>0?e:[]},d.search=function(b,c){return c?a.filter(b,function(a){var b=c.toLowerCase(),d=!1,e=a.title||"",f=a.chargeCode||"",g=a.pi||!1;return e.toLowerCase().indexOf(b)>-1?d=!0:f.toLowerCase().indexOf(b)>-1?d=!0:g&&(g.lastName.toLowerCase().indexOf(b)>-1||g.firstName.toLowerCase().indexOf(b)>-1||g.username.toLowerCase().indexOf(b)>-1||g.email.toLowerCase().indexOf(b)>-1)&&(d=!0),d}):angular.copy(b)},d.updateSelected=function(b,c,e){var f=[];for(var g in e)e[g]===!0&&f.push(g.toLowerCase());return c=d.search(b,e.search),0!==f.length?c=a.filter(c,function(b){var c=!1;return a.each(b.allocations,function(b){b.doNotShow=!0;var d=b.status.toLowerCase();a.contains(f,d)&&(b.doNotShow=!1,c=!0)}),c}):a.each(c,function(b){a.each(b.allocations,function(a){a.doNotShow=!1})}),c},d}]).factory("AllocationFactory",["$http","_","moment","NotificationFactory",function(a,b,c,d){var e={};return e.projects=[],e.userProjects=[],e.getAllocations=function(){var b="There was an error loading allocations.";return d.clearMessages("allocations"),d.addLoading("allocations"),a({method:"GET",url:"/admin/allocations/view/",cache:"true"}).then(function(a){d.removeLoading("allocations"),e.projects=a.data},function(){d.addMessage("allocations",b,"danger"),d.removeLoading("allocations")})},e.getUserAllocations=function(b){var c="There was an error loading user allocations.";return d.clearMessages("userAllocations"),d.addLoading("userAllocations"),a({method:"GET",url:"/admin/allocations/user/"+b+"/",cache:"true"}).then(function(a){d.removeLoading("userAllocations"),e.userProjects=a.data},function(){d.addMessage("userAllocations",c,"danger"),d.removeLoading("userAllocations")})},e.getProjectUsers=function(b){var c="projectUsers"+b.id,e="There was an error loading project users.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/projects/"+b.id+"/users/",cache:"true"}).then(function(a){d.removeLoading(c),b.users=a.data},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e}]).factory("UsageFactory",["$http","_","moment","NotificationFactory",function(a,b,c,d){var e={};e.projects=[],e.userProjects=[],e.downtimes=[],e.unused=[];var f=function(a,c){var d={},e=[];b.each(c.data,function(a){a[0]in d?d[a[0]]+=a[1]:d[a[0]]=a[1]}),b.each(b.keys(d),function(a){var b=[];b[0]=parseInt(a,10),b[1]=d[a],e.push(b)}),a.selectedAllocation.usage=b.sortBy(e,function(a){return a[0]})},g=function(a,c){var d={},e=[],f=[];for(var g in c.data){var h=c.data[g],i=0;for(var j in h)b.contains(f,j)||f.push(j),i+=h[j];e.push({user:g,total:i})}e=b.sortBy(e,"total").reverse();var k=b.pluck(e,"user");b.each(k,function(a){b.each(f,function(b){var e=c.data[a][b]||0;d.hasOwnProperty(b)||(d[b]=[]),d[b].push(Math.round(100*e)/100)})}),a.selectedAllocation.usageUsers=k,a.selectedAllocation.usageByUsers=d},h=function(a){var c=[];angular.forEach(a.data.result,function(a){c.push(["start",a.start,a.nodes_down]),a.end&&c.push(["end",a.end,a.nodes_down])}),c=b.sortBy(c,function(a){return a[1]});var d=0,f=50;angular.forEach(c,function(a){e.downtimes.push([a[1],d]),e.unused.push([a[1],f-d]),"start"===a[0]?d+=a[2]:"end"===a[0]&&(d-=a[2]),e.downtimes.push([a[1]+1e3,d]),e.unused.push([a[1]+1e3,f-d])})};return e.getAllocationUsage=function(b){var c="allocationUsage"+b.id,e="There was an error loading allocation usage.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/allocation/"+b.selectedAllocation.id+"/",cache:"true"}).then(function(a){d.removeLoading(c),f(b,a)},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e.getUsageByUsers=function(b){var e="usageByUsers"+b.id,f="There was an error loading usage by users.";d.clearMessages(e),d.addLoading(e);var h=c(b.from).utc().format("YYYY-MM-DDTHH:mm:ss")+"Z",i=c(b.to).utc().format("YYYY-MM-DDTHH:mm:ss")+"Z";return a({method:"GET",url:"/admin/usage/usage-by-users/"+b.selectedAllocation.id+"/?from="+h+"&to="+i,cache:"true"}).then(function(a){d.removeLoading(e),g(b,a)},function(){d.addMessage(e,f,"danger"),d.removeLoading(e)})},e.getAllocationUserUsage=function(b){var c="allocationUsage"+b.id,e="There was an error loading user allocation usage.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/allocation/"+b.selectedAllocation.id+"/username/"+b.selectedUser.username+"/",cache:"true"}).then(function(a){d.removeLoading(c),f(b,a)},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e.getAllocationUserQueueUsage=function(b){var c="allocationUsage"+b.id,e="There was an error loading user queue allocation usage.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/allocation/"+b.selectedAllocation.id+"/username/"+b.selectedUser.username+"/queue/"+b.selectedQueue+"/",cache:"true"}).then(function(a){d.removeLoading(c),f(b,a)},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e.getAllocationQueueUsage=function(b){var c="allocationUsage"+b.id,e="There was an error loading queue allocation usage.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/allocation/"+b.selectedAllocation.id+"/queue/"+b.selectedQueue+"/",cache:"true"}).then(function(a){d.removeLoading(c),f(b,a)},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e.getDowntimes=function(b){var c="downtimes",e="There was an error loading downtimes.";return d.clearMessages(c),d.addLoading(c),a({method:"GET",url:"/admin/usage/downtimes/",params:b,cache:"true"}).then(function(a){h(a),d.removeLoading(c)},function(){d.addMessage(c,e,"danger"),d.removeLoading(c)})},e}]),angular.module("usageApp").controller("UsageController",["$scope","$http","$timeout","$location","$filter","moment","highcharts","_","$modal","UtilFactory","AllocationFactory","NotificationFactory","UsageFactory",function(a,b,c,d,e,f,g,h,i,j,k,l,m){a.messages=[],a.$on("allocation:notifyMessage",function(){a.messages=l.getMessages()}),a.loading={},a.$on("allocation:notifyLoading",function(){a.loading=l.getLoading()}),a.close=j.closeMessage,a.isEmpty=j.isEmpty,a.hasMessage=j.hasMessage,a.isLoading=j.isLoading,a.getMessages=j.getMessages,a.getClass=j.getClass,a.filter={active:!0,inactive:!0,search:""},a.reset=function(){a.selectedProjects=a.projects,a.filter.active=!1,a.filter.inactive=!1,a.filter.search=""};var n={options:{chart:{zoomType:"x",type:"area"},rangeSelector:{enabled:!0,selected:2},navigator:{enabled:!0},colors:["#7cb5ec","#778b9e","#acf19d"],credits:{enabled:!1},plotOptions:{area:{dataLabels:{enabled:!0,color:g.theme&&g.theme.dataLabelsColor||"white",style:{textShadow:"0 0 3px black"}},fillOpacity:.5,marker:{enabled:!0,radius:3},shadow:!0,tooltip:{valueDecimals:2}},series:{lineWidth:1,dataLabels:{format:"{point.y:,.2f}"}}}},series:[],title:{text:""},useHighStocks:!0},o=angular.copy(n);o.options.yAxis={title:{text:"Percent"}},o.options.plotOptions.area.stacking="percent",o.options.plotOptions.area.marker={lineWidth:1,lineColor:"#ffffff"};var p={options:{chart:{type:"column"},xAxis:{categories:[]},yAxis:{min:0,title:{text:"Total SUs Used"},stackLabels:{enabled:!0,style:{fontWeight:"bold",color:g.theme&&g.theme.textColor||"gray"}}},legend:{align:"right",x:-30,verticalAlign:"top",y:25,floating:!0,backgroundColor:g.theme&&g.theme.background||"white",borderColor:"#CCC",borderWidth:1,shadow:!1},plotOptions:{column:{stacking:"normal",dataLabels:{enabled:!0,color:g.theme&&g.theme.dataLabelsColor||"white",style:{textShadow:"0 0 3px black"}}}},tooltip:{formatter:function(){return"<b>"+this.x+"</b><br/>"+this.series.name+": "+this.y+"<br/>Total: "+this.point.stackTotal}},credits:{enabled:!1}},title:{text:""},series:[]},q=function(a){for(var b=0;b<a.length;b++){var c=a[b];if(c.hasActiveAllocation=!1,!h.isEmpty(c.allocations))for(var d=0;d<c.allocations.length;d++)c.allocations[d].hasUsage=!1,h.contains(["active","inactive"],c.allocations[d].status.toLowerCase())&&(c.hasActiveAllocation=!0,c.allocations[d].hasUsage=!0,c.selectedAllocation||(c.selectedAllocation=c.allocations[d]))}};a.getAllocations=function(){a.projects=[],k.getAllocations().then(function(){a.projects=k.projects,q(a.projects),a.updateSelected()})},a.downtimes={from:null,to:null,startOpened:!1,endOpened:!1,selectedQueue:"",data:[]};var r=function(){a.downtimes.data=[];var b={};a.downtimes.from&&(b.from=f(a.downtimes.from).utc().format("YYYY-MM-DDTHH:mm:ss")+"Z"),a.downtimes.to&&(b.to=f(a.downtimes.to).utc().format("YYYY-MM-DDTHH:mm:ss")+"Z"),a.downtimes.selectedQueue&&(b.queue=a.downtimes.selectedQueue),m.getDowntimes(b).then(function(){a.downtimes.data=m.downtimes,a.downtimes.unused=m.unused,t()})};a.selections={usernamemodel:"",username:""},a.getUserAllocations=function(){a.projects=[],a.selections.username=a.selections.usernamemodel,d.url("/"+a.selections.username),a.submitted=!0,a.selections.username&&a.selections.username.length>0&&k.getUserAllocations(a.selections.username).then(function(){a.projects=k.userProjects,a.projects&&a.projects.length>0&&(q(a.projects),a.updateSelected())})},a.updateSelected=function(){a.selectedProjects=j.updateSelected(a.projects,a.selectedProjects,a.filter)},a.getAllocationsWithUsage=function(a){return h.filter(a.allocations,function(a){return a.hasUsage&&!a.doNotShow})};var s=function(a){a.usageChartConfig=angular.copy(n),a.usageChartConfig.title.text="Allocation Usage - "+a.selectedAllocation.resource+" ("+e("date")(a.selectedAllocation.start,"dd MMMM yyyy")+" - "+e("date")(a.selectedAllocation.end,"dd MMMM yyyy")+")",a.usageChartConfig.series=[],a.usageChartConfig.series.push({id:a.selectedAllocation.id,name:"SUs: ",data:a.selectedAllocation.usage,marker:{enabled:!0,radius:2},shadow:!0,tooltip:{valueDecimals:2}})},t=function(){a.downtimes.usageChartConfig=angular.copy(o),a.downtimes.usageChartConfig.title.text="Downtimes and Usage",a.downtimes.usageChartConfig.series=[],a.downtimes.usageChartConfig.series.push({id:"unused",name:"Nodes not used",data:a.downtimes.unused}),a.downtimes.usageChartConfig.series.push({id:"downtimes",name:"Nodes down",data:a.downtimes.data}),a.downtimes.usageChartConfig.series.push({id:"usage",name:"Nodes used",data:a.downtimes.data})},u=function(a){a.selectedUser?a.selectedQueue?m.getAllocationUserQueueUsage(a).then(function(){s(a)}):m.getAllocationUserUsage(a).then(function(){s(a)}):a.selectedQueue?m.getAllocationQueueUsage(a).then(function(){s(a)}):m.getAllocationUsage(a).then(function(){s(a)})};a.viewUsage=function(a){a.showUPUChart=!1,a.showChart=!0,k.getProjectUsers(a),u(a)};var v=function(a){a.usageByUserChartConfig=angular.copy(p),a.usageByUserChartConfig.title.text=e("date")(a.from,"dd MMMM yyyy")+" - "+e("date")(a.to,"dd MMMM yyyy"),a.usageByUserChartConfig.series=[],a.usageByUserChartConfig.options.xAxis.categories=a.selectedAllocation.usageUsers;for(var b in a.selectedAllocation.usageByUsers)a.usageByUserChartConfig.series.push({name:b,data:a.selectedAllocation.usageByUsers[b]})},w=function(a){m.getUsageByUsers(a).then(function(){v(a)})},x=function(b){b.from=a.getMinDate(b),b.to=a.getMaxDate(b)},y=function(){a.downtimes.from=a.getMinDowntimeDate(),a.downtimes.to=a.getMaxDowntimeDate()};a.viewUsagePerUser=function(a){a.from&&a.to||(a.dateRange="all",x(a)),a.showChart=!1,a.showUPUChart=!0,w(a)},a.updateUsageByUsersChart=function(a,b){switch(b){case"1m":a.dateRange="1m",a.from=f().startOf("day").subtract(1,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"3m":a.dateRange="3m",a.from=f().startOf("day").subtract(3,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"6m":a.dateRange="6m",a.from=f().startOf("day").subtract(6,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"ytd":a.dateRange="ytd",a.from=f().startOf("day").startOf("year").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"1y":a.dateRange="1y",a.from=f().startOf("day").subtract(1,"years").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"all":a.dateRange="all",x(a);break;default:a.dateRange="custom",a.from=f(a.from).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ"),a.to=f(a.to).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ")}w(a)},a.updateDowntimesUsageChart=function(b){switch(b){case"1m":a.downtimes.dateRange="1m",a.downtimes.from=f().startOf("day").subtract(1,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"3m":a.downtimes.dateRange="3m",a.downtimes.from=f().startOf("day").subtract(3,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"6m":a.downtimes.dateRange="6m",a.downtimes.from=f().startOf("day").subtract(6,"months").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"ytd":a.downtimes.dateRange="ytd",a.downtimes.from=f().startOf("day").startOf("year").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"1y":a.downtimes.dateRange="1y",a.downtimes.from=f().startOf("day").subtract(1,"years").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");break;case"all":a.downtimes.dateRange="all",y();break;default:a.downtimes.dateRange="custom",a.downtimes.from=f(a.downtimes.from).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ"),a.downtimes.to=f(a.downtimes.to).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ")}r()},a.viewUserUsage=function(b){b.showChart=!0,b.selectedUser={username:a.selections.username},u(b)},a.updateChart=function(a){u(a)},a.submitted=!1,a.handleKeyPress=function(b){var c=b.keyCode||b.which;13===c&&a.getUserAllocations()},a.dateOptions={formatYear:"yy",startingDay:1},a.format="dd MMMM yyyy",a.disabled=function(a,b){return!1},a.getMaxDate=function(a){var b=f().startOf("day").format("YYYY-MM-DDTHH:mm:ssZ");return f(a.selectedAllocation.end).isAfter(b,"day")?b:f(a.selectedAllocation.end).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ")},a.getMinDate=function(a){return f(a.selectedAllocation.start).startOf("day").format("YYYY-MM-DDTHH:mm:ssZ")},a.getMaxDowntimeDate=function(){return f().format("YYYY-MM-DDTHH:mm:ssZ")},a.getMinDowntimeDate=function(){return f("12-01-2014","MM-DD-YYYY").format("YYYY-MM-DDTHH:mm:ssZ")},a.open={},a.isOpen=function(a,b,c){a.preventDefault(),a.stopPropagation(),"start"===c?(b.endOpened=!1,b.startOpened=!0):"end"===c&&(b.startOpened=!1,b.endOpened=!0)},a.isOpen4Downtimes=function(b,c){b.preventDefault(),b.stopPropagation(),"start"===c?(a.downtimes.endOpened=!1,a.downtimes.startOpened=!0):"end"===c&&(a.downtimes.endOpened=!0,a.downtimes.startOpened=!1)};var z=d.path();z?(a.selections.usernamemodel=z.substring(1),a.getUserAllocations()):-1!==d.absUrl().indexOf("downtimes")?(y(),r()):a.getAllocations()}]);