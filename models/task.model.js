import mongoose from "mongoose";

const taskSchema = new mongoose.Schema(
    {
        username:{
            type:String,
            required:true
        },
        task:{
            type:String,
            required:true
        },
        complete:{
            type:Boolean,
            default:false
        },
        pending:{
            type:Boolean,
            default:false
        },
        skip:{
            type:Boolean,
            default:false
        }
    },{timestamps:true}
)

export const Task = mongoose.model("Task",taskSchema)