var todo = new Vue({
    el: '#todo',
    data: {
        newTask:"",
        updatedTask:"",
        todolist:[]
    },
    methods:{
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
        }
    }
})
