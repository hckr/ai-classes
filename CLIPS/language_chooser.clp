; Programming Language Chooser
; created by Jakub Młokosiewicz hckr.pl

; Open CLIPS shell and type the following to run:

; (load lang.clp)
; (reset)
; (run)

; Ctrl+C and then Enter to exit loop

(defrule main
	?x <- (initial-fact)
	=>
	(assert (start))
	(retract ?x)
	(printout t "** Programming language chooser **" crlf)
	(printout t "What do you want to make:" crlf))
	
(defrule webapp
	?x <- (start)
	(not (webapp ?))
	=>
	(retract ?x)
	(printout t "web app? (y/n) ")
	(assert (webapp(read))))
	
(defrule webapp-frontend
        ?x <- (webapp y)
        =>
        (retract ?x)
	(printout t "frontend? (y/n) ")
	(assert (webapp-frontend(read))))
	
(defrule webapp-frontend-strong-typing
        ?x <- (webapp-frontend y)
        =>
        (retract ?x)
	(printout t "do you prefer strong typing? (y/n) ")
	(assert (webapp-frontend-strong-typing(read))))

(defrule webapp-frontend-strong-typing-no
        ?x <- (webapp-frontend-strong-typing n)
        =>
        (retract ?x)
	(printout t "==> Choose JavaScript" crlf crlf)
	(assert (initial-fact)))
	
(defrule webapp-frontend-strong-typing-functional
        ?x <- (webapp-frontend-strong-typing y)
        =>
        (retract ?x)
	(printout t "do you prefer functional languages? (y/n) ")
	(assert (webapp-frontend-strong-typing-functional(read))))

(defrule webapp-frontend-strong-typing-functional-yes
        ?x <- (webapp-frontend-strong-typing-functional y)
        =>
        (retract ?x)
	(printout t "==> Choose Elm" crlf crlf)
	(assert (initial-fact)))

(defrule webapp-frontend-strong-typing-functional-no
        ?x <- (webapp-frontend-strong-typing-functional n)
        =>
        (retract ?x)
	(printout t "==> Choose TypeScript" crlf crlf)
	(assert (initial-fact)))
	
(defrule webapp-backend-functional
        ?x <- (webapp-frontend n)
        =>
        (retract ?x)
	(printout t "so backend it is. ")
	(printout t "do you prefer functional languages? (y/n) ")
	(assert (webapp-backend-functional(read))))

(defrule webapp-backend-functional-yes
        ?x <- (webapp-backend-functional y)
        =>
        (retract ?x)
	(printout t "==> Choose Scala" crlf crlf)
	(assert (initial-fact)))

(defrule webapp-backend-functional-no-business
        ?x <- (webapp-backend-functional n)
        =>
        (retract ?x)
	(printout t "is it a serious business grade solution? (y/n) ")
	(assert (webapp-backend-functional-no-business(read))))

(defrule webapp-backend-functional-no-business-yes
        ?x <- (webapp-backend-functional-no-business y)
        =>
        (retract ?x)
	(printout t "==> Choose Java or Kotlin" crlf crlf)
	(assert (initial-fact)))

(defrule webapp-backend-functional-no-business-no
        ?x <- (webapp-backend-functional-no-business n)
        =>
        (retract ?x)
	(printout t "==> Choose PHP or Python" crlf crlf)
	(assert (initial-fact)))
	
(defrule machine-learning
        ?x <- (webapp n)
        =>
        (retract ?x)
	(printout t "machine learning solution? (y/n) ")
	(assert (machine-learning(read))))

(defrule machine-learning-result
        ?x <- (machine-learning y)
        =>
        (retract ?x)
	(printout t "==> Choose Python" crlf crlf)
	(assert (initial-fact)))

(defrule desktop-app
        ?x <- (machine-learning n)
        =>
        (retract ?x)
	(printout t "desktop app? (y/n) ")
	(assert (desktop-app(read))))

(defrule desktop-app-multiplatform
        ?x <- (desktop-app y)
        =>
        (retract ?x)
	(printout t "should it be multiplatform? (y/n) ")
	(assert (desktop-app-multiplatform(read))))

(defrule desktop-app-multiplatform-yes-result
        ?x <- (desktop-app-multiplatform y)
        =>
        (retract ?x)
	(printout t "==> Choose C++ with Qt" crlf crlf)
	(assert (initial-fact)))

(defrule desktop-app-windows
        ?x <- (desktop-app-multiplatform n)
        =>
        (retract ?x)
	(printout t "windows only? (y/n) ")
	(assert (desktop-app-windows(read))))

(defrule desktop-app-windows-result
        ?x <- (desktop-app-windows y)
        =>
        (retract ?x)
	(printout t "==> Choose C# with .NET" crlf crlf)
	(assert (initial-fact)))

(defrule desktop-app-macos
        ?x <- (desktop-app-windows n)
        =>
        (retract ?x)
	(printout t "macos only? (y/n) ")
	(assert (desktop-app-macos(read))))

(defrule desktop-app-macos-result
        ?x <- (desktop-app-macos y)
        =>
        (retract ?x)
	(printout t "==> Choose Swift or Objective-C" crlf crlf)
	(assert (initial-fact)))

(defrule desktop-app-linux
        ?x <- (desktop-app-macos n)
        =>
        (retract ?x)
	(printout t "linux only? (y/n) ")
	(assert (desktop-app-linux(read))))

(defrule desktop-app-linux-result
        ?x <- (desktop-app-linux y)
        =>
        (retract ?x)
	(printout t "==> Choose any language with Qt or GTK+ support" crlf crlf)
	(assert (initial-fact)))

(defrule desktop-app-other-result
        ?x <- (desktop-app-linux n)
        =>
        (retract ?x)
	(printout t "I'm sorry, I don't support other OSes. Try C++ and Qt?" crlf crlf)
	(assert (initial-fact)))

(defrule mobile-app
        ?x <- (desktop-app n)
        =>
        (retract ?x)
	(printout t "mobile app? (y/n) ")
	(assert (mobile-app(read))))

(defrule mobile-app-multiplatform
        ?x <- (mobile-app y)
        =>
        (retract ?x)
	(printout t "should it be multiplatform? (y/n) ")
	(assert (mobile-app-multiplatform(read))))

(defrule mobile-app-multiplatform-yes-result
        ?x <- (mobile-app-multiplatform y)
        =>
        (retract ?x)
	(printout t "==> Choose Dart with Flutter" crlf crlf)
	(assert (initial-fact)))

(defrule mobile-app-android
        ?x <- (mobile-app-multiplatform n)
        =>
        (retract ?x)
	(printout t "android only? (y/n) ")
	(assert (mobile-app-android(read))))

(defrule mobile-app-android-result
        ?x <- (mobile-app-android y)
        =>
        (retract ?x)
	(printout t "==> Choose Kotlin or Java" crlf crlf)
	(assert (initial-fact)))

(defrule mobile-app-ios
        ?x <- (mobile-app-android n)
        =>
        (retract ?x)
	(printout t "ios only? (y/n) ")
	(assert (mobile-app-ios(read))))

(defrule mobile-app-ios-result
        ?x <- (mobile-app-ios y)
        =>
        (retract ?x)
	(printout t "==> Choose Swift" crlf crlf)
	(assert (initial-fact)))

(defrule mobile-app-other-result
        ?x <- (mobile-app-ios n)
        =>
        (retract ?x)
	(printout t "I'm sorry, I don't support other OSes" crlf crlf)
	(assert (initial-fact)))

(defrule catch-all
        ?x <- (mobile-app n)
        =>
        (retract ?x)
	(printout t "I'm sorry, I don't support other types yet" crlf crlf)
	(assert (initial-fact)))
