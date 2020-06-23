<template>
    <div id="todo">
        <h3>TDL</h3>
        <input 
            type="text" 
            placeholder="Add new task"
            v-model="newTask" 
            @keyup.enter="addTask(newTask)" 
        />
        <button @click="addTask(newTask)">Add</button>

        <ul>
            <li v-for="(todo,index) in todolist" :key='index' v-bind:class="{ active: todo.complete }">
                <input type="checkbox" v-model="todo.complete">
                {{todo.content}}
                <button @click="deleteTask(todo)">Delete</button>
                <button 
                    @click="updateTrigger(todo)" 
                    v-if="!todo.update"
                >Edit</button>
                <input
                    v-if="todo.update"
                    type="text" 
                    v-model="updatedTask" 
                    @keyup.enter="updateTask(todo,updatedTask);updateTrigger(todo)" 
                    placeholder="Type new task here"
                >
                <button 
                    v-if="todo.update" 
                    @click="updateTask(todo,updatedTask);updateTrigger(todo)"
                >Update</button>                
                <button 
                    v-if="todo.update" 
                    @click="updateTrigger(todo)" 
                >Cancel</button>
            </li>
        </ul>
        
        <br>
        <!-- <p>{{fetchedData}}</p> -->

        <!-- 後端資料 -->
        <h3>API</h3>
        <input 
            type="text" 
            placeholder="Add new task"
            v-model="apiNewTask" 
            @keyup.enter="apiAdd(apiNewTask)"
        />
        <button @click="apiAdd(apiNewTask)">Add</button>
        <br>

        <ul>
            <li v-for="(item,index) in fetchedData" :key='index'>
                <input type="checkbox" v-model="item[2]" @click="apiSwitch(item[0])">
                {{item[0]}},
                {{item[1]}},
                {{item[2]}}
                <!-- ,{{item[3]}}, -->
                <!-- {{item[4]}} -->
                <button @click="apiDelete(item[0])">Delete</button>
                <!-- <button @click="apiEditOn(item[0])" v-if="!item[3]">Edit</button> -->
                <input type="text" v-if="item[3]" v-model="item[4]" @keyup.enter="apiEdit(item[0],item[4])">
                <button @click="apiEdit(item[0],item[4])" v-if="item[3]" >Update</button>
                <button @click="apiEditOff(item[0])" v-if="item[3]">Cancel</button>
            </li>
        </ul>

        <pre>
            <!-- {{this.todolist}} -->
        </pre>
          
    </div>
</template>

<script>
    // @ is an alias to /src
    // import HelloWorld from "@/components/HelloWorld.vue"; //把html引用進來
    export default {
        //暴露出來讓Vue.app可以吃到
        name: "Todo", //自己取的名字，最好跟檔名一樣
        data(){
            return {
                newTask:"",
                updatedTask:"",
                todolist:[],
                fetchedData:{},
                apiNewTask:"",
                apiUpdateData:[],
            }
        },
        created(){
            this.getRequest()
        },
        methods:{
            getRequest(){
                fetch('http://127.0.0.1:5000/')
                    .then(response => { 
                        return  response.json() })
                    .then(json =>{
                        this.fetchedData = json
                    })
            },
            addTask(newTask){
                if (this.newTask !== ""){
                    this.todolist.push({content: newTask, complete: false, update: false})
                    this.newTask=""    
                }
            },
            deleteTask(task){
                this.todolist.splice(this.todolist.indexOf(task),1)
            },
            updateTask(task, updatedTask){
                if (this.updatedTask !== ""){
                    this.todolist[this.todolist.indexOf(task)].content = updatedTask
                    this.updatedTask=""    
                }
            },
            updateTrigger(task){
                if (this.todolist[this.todolist.indexOf(task)].update){
                    this.todolist[this.todolist.indexOf(task)].update=false
                }else{
                    this.todolist[this.todolist.indexOf(task)].update=true
                }
            },
            apiReload(json){
                this.fetchedData=[]
                this.fetchedData.push(json)
                this.fetchedData = this.fetchedData.flat()
            },
            apiDone(task_id){
                const url='http://127.0.0.1:5000/done/'+Number(task_id)
                fetch(url, {method:'PUT'})
                    .then(response => response.json())
                    .then(json => this.apiReload(json))       
            },
            apiUndo(task_id){
                const url='http://127.0.0.1:5000/undo/'+Number(task_id)
                fetch(url, {method:'PUT'})
                    .then(response => response.json())
                    .then(json => this.apiReload(json))       
            },
            apiSwitch(task_id){
                for (let i=0; i<this.fetchedData.length; i++){
                    if (this.fetchedData[i][0] === task_id){
                        if (this.fetchedData[i][2] === 0){
                            this.apiDone(this.fetchedData[i][0])
                        }else if(this.fetchedData[i][2] === 1){
                            this.apiUndo(this.fetchedData[i][0])
                        }
                    }
                }
            },
            apiAdd(apiNewTask){
                const req = new Request('http://127.0.0.1:5000/add', {
                    method: 'POST',
                    body: JSON.stringify({
                        'content': apiNewTask
                    })
                })
                fetch(req)
                    .then(response => response.json())
                    .then(json => this.apiReload(json))     
                this.apiNewTask=""
            },
            apiDelete(task_id){
                const url='http://127.0.0.1:5000/delete/'+Number(task_id)
                fetch(url, {method:'DELETE'})
                    .then(response => response.json())
                    .then(json => this.apiReload(json)) 
            },
            apiEditOn(task_id){
                const url='http://127.0.0.1:5000/editon/'+Number(task_id)
                fetch(url, {method:'PUT'})
                    .then(response => response.json())
                    .then(json => this.apiReload(json))       
            },            
            apiEditOff(task_id){
                const url='http://127.0.0.1:5000/editoff/'+Number(task_id)
                fetch(url, {method:'PUT'})
                    .then(response => response.json())
                    .then(json => this.apiReload(json))       
            },
            apiEdit(task_id, editedTask){
                const url='http://127.0.0.1:5000/edit/'+Number(task_id)
                // const urlEdit = 'http://127.0.0.1:5000/editoff/'+Number(task_id)
                const req = new Request(url, {
                    method: 'PUT',
                    body: JSON.stringify({
                        'content': editedTask
                    })
                })
                fetch(req)
                    .then(response => response.json())
                    .then(json => this.apiReload(json))
                // fetch(urlEdit, {method:'PUT'})
                //     .then(response => response.json())
                //     .then(json => this.apiReload(json))       

            }
        }
    //components: {
    //  HelloWorld //我要把他變成html標籤 <HelloWorld>
    //}
    };
</script>
