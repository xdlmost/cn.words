class Calendar
{
    selectedDate=null;
    validDateList=[];
    months=['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'];
    showDate=null;
    getSearchString= function (key, Url) 
        {
            var str = Url;
            str = str.substring(1, str.length); 
            var arr = str.split("&");
            var obj = new Object();
            for (var i = 0; i < arr.length; i++) {
                var tmp_arr = arr[i].split("=");
                obj[decodeURIComponent(tmp_arr[0])] = decodeURIComponent(tmp_arr[1]);
            }
        return obj[key];
        }
    isValidDate=function(date) {
        return date instanceof Date && !isNaN(date.getTime());
    }
    strToDate=function(str){
        return new Date(str);
    }
    nextMonth=function(){
        var year=this.showDate.getFullYear();
        var month=this.showDate.getMonth()+1;
        var s='';
        if (month>=12){
            s=(year+1).toString()+'-1-1';
        }else{
            s=year.toString()+'-'+(month+1).toString()+'-1';
        }
        this.changeTo(s);
    }
    preMonth=function(){
        var year=this.showDate.getFullYear();
        var month=this.showDate.getMonth()+1;
        var s='';
        if (month<=1){
            s=(year-1).toString()+'-12-1';
        }else{
            s=year.toString()+'-'+(month-1).toString()+'-1';
        }
        this.changeTo(s);
    }
    changeTo=function(showdatestr){
        var showDate=this.strToDate(showdatestr);
        this.showDate=showDate;
        var month=showDate.getMonth();
        var header=document.getElementById('calendar-title');
        while(header.hasChildNodes()) 
        {
        　　header.removeChild(header.firstChild);
        }
        var table_body=document.getElementById('calendar-body');
        while(table_body.hasChildNodes()) 
        {
            table_body.removeChild(table_body.firstChild);
        }
        var left=document.createElement('a');
        left.setAttribute('href','javascript:hehe.preMonth();');
        left.classList.add('to-month');
        left.innerText='<';

        var right=document.createElement('a');
        right.setAttribute('href','javascript:hehe.nextMonth();');
        right.classList.add('to-month');
        right.innerText='>';

        var monthDiv=document.createElement('span');
        monthDiv.classList.add('month');
        monthDiv.innerText='    '+showDate.getFullYear()+'-'+this.months[month]+'    ';

        header.appendChild(left);
        header.appendChild(monthDiv);
        header.appendChild(right);

        var firstDate=new Date(showDate);
        firstDate.setDate(1);
        var lastDate=new Date(showDate);
        for (var i=29;i<32;i++){
            lastDate.setDate(i);
            if(lastDate.getMonth()!=month){
                lastDate=new Date(showDate.getFullYear(),month,i-1);
                break;
            }
        }
        var lineIndex=0;
        var c=[];
        var indexDate=firstDate;
        while(indexDate.getDate()!=lastDate.getDate()){
            if(c.length<lineIndex+1){
                c.push([0,0,0,0,0,0,0]);
            }
            c[lineIndex][indexDate.getDay()]=indexDate.getDate();
            if(6==indexDate.getDay()){
                lineIndex++;
            }
            indexDate.setDate(indexDate.getDate()+1);
        }

        for (var item of c){
            var tr=document.createElement('tr');
            for (var i of item){
                var td=document.createElement('td');
                if(0!=i){
                    var s=this.showDate.getFullYear().toString()+'-'+(this.showDate.getMonth()+1).toString()+'-'+i.toString();
                    if(this.validDateList.indexOf(s)!=-1){
                        var a=document.createElement('a');
                        a.setAttribute('href','/review/'+s+'?uid='+this.getSearchString("uid",window.location.search));
                        a.innerHTML=i;
                        td.appendChild(a);
                    }else{
                        td.innerText=i;
                    }
                    if (s==this.selectedDate){
                        td.setAttribute('style','background:#e66b6b;');
                    }

                }else{

                }
                tr.appendChild(td);
            }
            table_body.appendChild(tr);
        }

    }
    constructor(validDateStrList,selectedDateStr) 
    { 
        this.selectedDate=selectedDateStr;
        this.showDate=this.strToDate(selectedDateStr);
        this.showDate.setDate(1);
        this.validDateList=validDateStrList;
        this.changeTo(selectedDateStr);
    }
}


