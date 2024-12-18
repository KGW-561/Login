package com.team3.scvs.repository;

import com.team3.scvs.entity.ForexEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ForexRepository extends JpaRepository<ForexEntity, Long> {
    Optional<ForexEntity> findByForexName(String forexName);
}
