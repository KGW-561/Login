package com.team3.scvs.controller;

import com.team3.scvs.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

/**
 * 로그인이 되면 모든 컨트롤러에 대해서
 * 공통적으로 userId값을 집어 넣어서 개인 정보 접근 가능케 하기 위한 클래스
 */
@ControllerAdvice
public class UserControllerAdvice {
    @Autowired
    private UserService userService;

    @ModelAttribute
    public void addAttributes(Model model) {
        String authenticatedUsername = userService.getAuthenticatedUsername();
        if (authenticatedUsername != null) {
            Long userId = userService.getUserId(authenticatedUsername);
            model.addAttribute("userId", userId);
        }
    }
}
