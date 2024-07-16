import express from "express"
import mongoose from "mongoose"
import 'dotenv/config'
import cors from "cors"
import { Task } from "./models/task.model.js";
import bodyparser from "body-parser"



//specs
const app = express();
const port = process.env.PORT || 5000

//middlewares
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(cors())
app.use(bodyparser.json())


//dbconnection
const dbConnect = async () => {
    try {
        const connection = await mongoose.connect(`${process.env.MONGODB_URI}/task-manager`);
        console.log("DB Connected!!")
    } catch (error) {
        console.error(error)
    }
    
}
dbConnect();


//routes
//to add task
app.post("/api/addtask", async (req,res) => {
    const {username,task} = req.body;
    try {
        const addTask = await Task.create({username,task});
        res.status(200).json(
            {
                message:"Task added successfully",
                name:username,
                task:task
            }
        )
        
    } catch (error) {
        res.status(500).json(
            {
                message:"Error adding task!!",
                error
            }
        )
    }
})

//to query tasks
app.post("/api/gettasks", async (req,res) => {
    const {username} = req.body;
    try {
        const registeredUser = await Task.find({username});
        if (registeredUser == "") {
            res.status(404).send(`${username} user has no tasks!!`)
            
        } else {
            res.status(200).json(registeredUser)
        }
        
    } catch (error) {
        res.status(500).send("Error finding the task!!")
    }
})

//to update a task
app.put("/api/updatetask", async (req,res) => {
    const {username,task,complete,pending,skip} = req.body;
    const existingUser = await Task.findOne({username,task});
    try {
        if (existingUser) {
            const updateBooolean = await Task.updateOne(
                {task:task, username:username},{complete,pending,skip}
            );
            const updatedUser = await Task.findOne({username,task})
            res.status(200).send(updatedUser);
            
        }
        else{
            res.status(404).send(`${username} and ${task} does not exist!!`)
        }
    } catch (error) {
        res.status(404).send(error);
    }

})

//to delete a task
app.post("/api/deletetask", async (req,res) => {
    const {username,task} = req.body;
    const existingUser = await Task.findOne({username,task});
    try {
        if (existingUser) {
            const deleteTask = await Task.deleteOne({username,task});
            res.status(200).send(`Task:${task} of username: ${username} has been deleted`);
        }
        else{
            res.status(404).send(`${username} and ${task} does not exist!!`)
        }
    } catch (error) {
        res.status(404).send(error);
    }
})












try {
    app.listen(port , (req,res) => {
        console.log(`App is listening on port ${port}`)
    })
} catch (error) {
    console.error(error)
}








