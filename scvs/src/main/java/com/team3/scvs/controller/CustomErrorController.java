package com.team3.scvs.controller;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.http.HttpServletRequest;
import org.apache.hc.core5.http.HttpStatus;
import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
public class CustomErrorController implements ErrorController {

    @RequestMapping("/error")
    public String handleError(HttpServletRequest request){
        Object status = request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);

        if(status != null){
            int statusCode = Integer.parseInt(status.toString());

            if(statusCode == HttpStatus.SC_NOT_FOUND){
                return "error/404";
            }
            else if(statusCode == HttpStatus.SC_INTERNAL_SERVER_ERROR){
                return "error/500";
            }

        }
        return "error";
    }

    public String getErrorPath(){
        return "/error";
    }
}
