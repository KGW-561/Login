package com.team3.scvs.entity;

import jakarta.persistence.*;
import jakarta.persistence.Entity;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.format.annotation.DateTimeFormat;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "psa")
public class PSAEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "psa_id")
    private Long id; // 공지사항 ID (Primary Key)

    @Column(name = "title", nullable = false, length = 255)
    private String title; // 공지사항 제목

    @Column(name = "content", nullable = false, columnDefinition = "TEXT")
    private String content; // 공지사항 내용

    @Column(name = "published_at", nullable = false, updatable = false)
    private LocalDateTime publishedAt; // 공지사항 작성 시간

    @PrePersist
    protected void onCreate() {
        this.publishedAt = LocalDateTime.now();
    }
}

