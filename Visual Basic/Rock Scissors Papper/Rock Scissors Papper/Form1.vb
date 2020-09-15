'Kámen, nůžky, papír
'Yana Zabrodskaya, T1
'UJOP, 2016/2017
'Programování

Public Class Form1
    Dim userChoise As String = " " 'výběr (prvního) uživatele v Easy Level
    Dim secondUserChoise As String = " " 'výběr druhého uživatele v Easy Level
    Dim choiseFor5 As String = " " 'výběr (prvního) uživatele v Hard Level
    Dim secondChoiseFor5 As String = " " 'výběr druhého uživatele v Hard Level
    Dim compChoise As Integer = CInt(Int((100 * Rnd()) + 1)) 'počítání vybera počítače (random od 0 do 100)
    Dim hint As Integer = CInt(Int((100 * Rnd()) + 1)) 'počítání možnosti nápovědy (random od 0 do 100)
    Dim computerChoise As String 'zachovávání compChoise v String
    Dim win As Integer = 0 'počet výher
    Dim loose As Integer = 0 'počet proher
    Dim nGames As Integer = 0 'počet her celkem
    Dim name1 As String  'first user's name
    Dim name2 As String  'second user's name

    'CompChoise for Rock Scissors Papper
    Private Function RSP() 'CompChoise je random

        If compChoise < 34 Then
            computerChoise = "rock"
        ElseIf compChoise < 67 Then
            computerChoise = "scissors"
        Else
            computerChoise = "papper"
        End If
        Return computerChoise
    End Function

    'CompChoise for Rock Scissors Papper Lizard Spock
    Private Function RSPLS() 'compChoise je random

        If compChoise < 21 Then
            computerChoise = "rock"
        ElseIf compChoise < 41 Then
            computerChoise = "scissors"
        ElseIf compChoise < 61 Then
            computerChoise = "papper"
        ElseIf compChoise < 81 Then
            computerChoise = "lizard"
        Else
            computerChoise = "Spock"
        End If
        Return computerChoise
    End Function

    'starts
    Private Sub Start()
        Randomize()
        compChoise = CInt(Int((100 * Rnd()) + 1)) 'nový CompChoise
        'userChoise = " "
        ToolStripMenuItem1.Visible = True 'hint
    End Sub
    Private Sub Start2()
        userChoise = " " 'nový výběr prvního uživatele
        secondUserChoise = " " 'nový výběr druhého uživatele

        rock.Visible = True
        scissors.Visible = True
        papper.Visible = True
        rock2.Visible = True
        scissors2.Visible = True
        papper2.Visible = True
    End Sub
    Private Sub Start5()
        Randomize()
        compChoise = CInt(Int((100 * Rnd()) + 1)) 'nový CompChoise
        'choiseFor5 = " "
        ToolStripMenuItem1.Visible = True 'hint
    End Sub
    Private Sub Start5_2()
        choiseFor5 = " " 'nový výběr prvního uživatele
        secondChoiseFor5 = " " 'nový výběr druhého uživatele

        RadioButton4.Visible = True
        RadioButton5.Visible = True
        RadioButton6.Visible = True
        RadioButton7.Visible = True
        RadioButton8.Visible = True
        RadioButton9.Visible = True
        RadioButton10.Visible = True
        RadioButton11.Visible = True
        RadioButton12.Visible = True
        RadioButton13.Visible = True

    End Sub

    'EASY user vs pc
    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click
        RSP() 'dostaneme CompChoise
        If userChoise = " " Then 'jestli user ničeho nevybral
            MsgBox("choose at least anything, please")
            Label2.Text = " " 'výběr uživatele
            Label3.Text = " " 'výběr počítače
        Else
            Label3.Text = "computer's choise was " & computerChoise 'výběr počítače
            Label2.Text = "your choise was " & userChoise 'výběr uživatele
            If computerChoise = userChoise Then 'remisa
                MsgBox("in a draw")
                nGames += 1 'počet her celkem
            ElseIf userChoise = "rock" Then
                If computerChoise = "scissors" Then
                    MsgBox("you won")
                    win += 1 'kolik her vyhrál user
                    nGames += 1
                Else
                    MsgBox("you lost")
                    loose += 1 'kolik her prohrál user
                    nGames += 1
                End If
            ElseIf userChoise = "scissors" Then
                If computerChoise = "papper" Then
                    MsgBox("you won")
                    win += 1
                    nGames += 1
                Else
                    MsgBox("you lost")
                    loose += 1
                    nGames += 1
                End If
            ElseIf userChoise = "papper" Then
                If computerChoise = "rock" Then
                    MsgBox("you won")
                    win += 1
                    nGames += 1
                Else
                    MsgBox("you lost")
                    loose += 1
                    nGames += 1
                End If
            End If
        End If
        'RadioButton1.Checked = False
        'RadioButton2.Checked = False
        'RadioButton3.Checked = False
        Start() 'počítání nového výběru počítače

        Label17.Text = "You" & vbCrLf & win 'score
        Label18.Text = "Computer" & vbCrLf & loose 'score
        If nGames = 10 Then 'když počet her = 10, game over
            MsgBox("Game Over" & vbCrLf & "your score: won " & win & " : lost " & loose)
            win = 0
            loose = 0
            nGames = 0
        End If

    End Sub
    'user choise
    Private Sub RadioButton1_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton1.CheckedChanged
        userChoise = "rock"
    End Sub
    Private Sub RadioButton2_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton2.CheckedChanged
        userChoise = "scissors"
    End Sub
    Private Sub RadioButton3_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton3.CheckedChanged
        userChoise = "papper"
    End Sub
    'clicks on pictures
    Private Sub PictureBox1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox1.Click
        userChoise = "rock"
        RadioButton1.Checked = True
        Button1_Click(sender, e)

    End Sub
    Private Sub PictureBox2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox2.Click
        userChoise = "scissors"
        RadioButton2.Checked = True
        Button1_Click(sender, e)
    End Sub
    Private Sub PictureBox3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox3.Click
        userChoise = "papper"
        RadioButton3.Checked = True
        Button1_Click(sender, e)
    End Sub


    'EASY user vs user
    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click
        If userChoise = " " And secondUserChoise = " " Then 'jestli user1 a user2 nic nemájí
            MsgBox("choose at least anything, please")
            Label5.Text = " "
            Label6.Text = " "
        ElseIf userChoise = " " Or secondUserChoise = " " Then 'jestli user1 nebo user2 nic nemá
            MsgBox("choose at least anything, please")
            Label5.Text = " "
            Label6.Text = " "
        Else
            Label5.Text = name2 & "'s choise was " & secondUserChoise 'výběry uživatelů
            Label6.Text = name1 & "'s choise was " & userChoise 'výběry uživatelů
            If secondUserChoise = userChoise Then
                MsgBox("in a draw")
                nGames += 1 'počet her celkem 
            ElseIf userChoise = "rock" Then
                If secondUserChoise = "scissors" Then
                    MsgBox(name1 & " won")
                    nGames += 1
                    win += 1 'počet výher prvního uživatele
                Else
                    MsgBox(name2 & " won")
                    nGames += 1
                    loose += 1 'počet výher druhého uživatele
                End If
            ElseIf userChoise = "scissors" Then
                If secondUserChoise = "papper" Then
                    MsgBox(name1 & " won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    nGames += 1
                    loose += 1
                End If
            ElseIf userChoise = "papper" Then
                If secondUserChoise = "rock" Then
                    MsgBox(name1 & " won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    nGames += 1
                    loose += 1
                End If
            End If
        End If
        Label17.Text = name1 & vbCrLf & win 'score
        Label18.Text = name2 & vbCrLf & loose 'score
        If nGames = 10 Then
            MsgBox("Game Over" & vbCrLf & "your score: " & name1 & " " & win & " : " & name2 & " " & loose)
            win = 0
            loose = 0
            nGames = 0
        End If

        Start2()
    End Sub
    'user1 choise
    Private Sub rock_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles rock.CheckedChanged
        userChoise = "rock"
        'aby druhý user neviděl výběr
        rock.Checked = False
        scissors.Checked = False
        papper.Checked = False
        rock.Visible = False
        scissors.Visible = False
        papper.Visible = False
    End Sub
    Private Sub scissors_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles scissors.CheckedChanged
        userChoise = "scissors"
        'aby druhý user neviděl výběr
        rock.Checked = False
        scissors.Checked = False
        papper.Checked = False
        rock.Visible = False
        scissors.Visible = False
        papper.Visible = False
    End Sub
    Private Sub papper_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles papper.CheckedChanged
        userChoise = "papper"
        'aby druhý user neviděl výběr
        rock.Checked = False
        scissors.Checked = False
        papper.Checked = False
        rock.Visible = False
        scissors.Visible = False
        papper.Visible = False
    End Sub
    'user2 choise
    Private Sub rock2_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles rock2.CheckedChanged
        secondUserChoise = "rock"
        'aby první user neviděl výběr
        rock2.Checked = False
        scissors2.Checked = False
        papper2.Checked = False
        rock2.Visible = False
        scissors2.Visible = False
        papper2.Visible = False
    End Sub
    Private Sub scissors2_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles scissors2.CheckedChanged
        secondUserChoise = "scissors"
        'aby první user neviděl výběr
        rock2.Checked = False
        scissors2.Checked = False
        papper2.Checked = False
        rock2.Visible = False
        scissors2.Visible = False
        papper2.Visible = False
    End Sub
    Private Sub papper2_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles papper2.CheckedChanged
        secondUserChoise = "papper"
        'aby první user neviděl výběr
        rock2.Checked = False
        scissors2.Checked = False
        papper2.Checked = False
        rock2.Visible = False
        scissors2.Visible = False
        papper2.Visible = False
    End Sub
    'clicks on pictures
    Private Sub PictureBox4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox4.Click
        If userChoise = "rock" Or userChoise = "scissors" Or userChoise = "papper" Then
            secondUserChoise = "papper"
            'aby první user neviděl výběr
            rock2.Checked = False
            scissors2.Checked = False
            papper2.Checked = False
            rock2.Visible = False
            scissors2.Visible = False
            papper2.Visible = False
            Button2_Click(sender, e)

        Else
            userChoise = "papper"
            'aby druhý user neviděl výběr
            rock.Checked = False
            scissors.Checked = False
            papper.Checked = False
            rock.Visible = False
            scissors.Visible = False
            papper.Visible = False
            If secondUserChoise = "rock" Or secondUserChoise = "scissors" Or secondUserChoise = "papper" Then
                Button2_Click(sender, e)
            End If
        End If

    End Sub
    Private Sub PictureBox5_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox5.Click
        If userChoise = "rock" Or userChoise = "scissors" Or userChoise = "papper" Then
            secondUserChoise = "scissors"
            'aby první user neviděl výběr
            rock2.Checked = False
            scissors2.Checked = False
            papper2.Checked = False
            rock2.Visible = False
            scissors2.Visible = False
            papper2.Visible = False
            Button2_Click(sender, e)

        Else
            userChoise = "scissors"
            'aby druhý user neviděl výběr
            rock.Checked = False
            scissors.Checked = False
            papper.Checked = False
            rock.Visible = False
            scissors.Visible = False
            papper.Visible = False
            If secondUserChoise = "rock" Or secondUserChoise = "scissors" Or secondUserChoise = "papper" Then
                Button2_Click(sender, e)
            End If
        End If
    End Sub
    Private Sub PictureBox6_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox6.Click
        If userChoise = "rock" Or userChoise = "scissors" Or userChoise = "papper" Then
            secondUserChoise = "rock"
            'aby první user neviděl výběr
            rock2.Checked = False
            scissors2.Checked = False
            papper2.Checked = False
            rock2.Visible = False
            scissors2.Visible = False
            papper2.Visible = False
            Button2_Click(sender, e)

        Else
            userChoise = "rock"
            'aby druhý user neviděl výběr
            rock.Checked = False
            scissors.Checked = False
            papper.Checked = False
            rock.Visible = False
            scissors.Visible = False
            papper.Visible = False
            If secondUserChoise = "rock" Or secondUserChoise = "scissors" Or secondUserChoise = "papper" Then
                Button2_Click(sender, e)
            End If
        End If
    End Sub

    'HARD user vs pc
    Private Sub Button3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button3.Click
        RSPLS() 'dostaneme CompChoise

        'všechno je stejné jako v EASY user vs pc, kromě toho, že je 5 možnosti výběru
        If choiseFor5 = " " Then
            MsgBox("choose at least anything, please")
            Label12.Text = " "
            Label11.Text = " "
        Else
            Label11.Text = "computer's choise was " & computerChoise
            Label12.Text = "your choise was " & choiseFor5
            If computerChoise = choiseFor5 Then
                MsgBox("in a draw")
                nGames += 1
            ElseIf choiseFor5 = "rock" Then
                If computerChoise = "scissors" Or computerChoise = "lizard" Then
                    MsgBox("you won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox("you lost")
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "scissors" Then
                If computerChoise = "papper" Or computerChoise = "lizard" Then
                    MsgBox("you won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox("you lost")
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "papper" Then
                If computerChoise = "rock" Or computerChoise = "Spock" Then
                    MsgBox("you won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox("you lost")
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "lizard" Then
                If computerChoise = "papper" Or computerChoise = "Spock" Then
                    MsgBox("you won")
                    win += 1
                    nGames += 1
                Else
                    MsgBox("you lost")
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "Spock" Then
                If computerChoise = "rock" Or computerChoise = "scisors" Then
                    MsgBox("you won")
                    nGames += 1
                    win += 1
                Else
                    MsgBox("you lost")
                    nGames += 1
                    loose += 1
                End If
            End If
        End If
        Label17.Text = "You" & vbCrLf & win
        Label18.Text = "Computer" & vbCrLf & loose
        If nGames = 10 Then
            MsgBox("Game Over" & vbCrLf & "your score: won " & win & " : lost " & loose)
            win = 0
            loose = 0
            nGames = 0
        End If

        ' rock5.Checked = False
        ' scissors5.Checked = False
        ' papper5.Checked = False
        ' lizard5.Checked = False
        ' spock5.Checked = False
        Start5()

    End Sub
    'user choise
    Private Sub rock5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles rock5.CheckedChanged
        choiseFor5 = "rock"
    End Sub
    Private Sub scissors5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles scissors5.CheckedChanged
        choiseFor5 = "scissors"
    End Sub
    Private Sub papper5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles papper5.CheckedChanged
        choiseFor5 = "papper"
    End Sub
    Private Sub lizard5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles lizard5.CheckedChanged
        choiseFor5 = "lizard"
    End Sub
    Private Sub spock5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles spock5.CheckedChanged
        choiseFor5 = "Spock"
    End Sub
    'clicks on pictures
    Private Sub PictureBox7_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox7.Click
        choiseFor5 = "papper"
        papper5.Checked = True
        Button3_Click(sender, e)
    End Sub
    Private Sub PictureBox8_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox8.Click
        choiseFor5 = "scissors"
        scissors5.Checked = True
        Button3_Click(sender, e)
    End Sub
    Private Sub PictureBox9_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox9.Click
        choiseFor5 = "rock"
        rock5.Checked = True
        Button3_Click(sender, e)
    End Sub
    Private Sub PictureBox10_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox10.Click
        choiseFor5 = "lizard"
        lizard5.Checked = True
        Button3_Click(sender, e)
    End Sub
    Private Sub PictureBox11_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox11.Click
        choiseFor5 = "Spock"
        spock5.Checked = True
        Button3_Click(sender, e)
    End Sub

    'HARD user vs user
    Private Sub Button4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button4.Click
        'všechno je stejné jako v EASY user vs user, kromě toho, že je 5 možnosti výběru
        If choiseFor5 = " " And secondChoiseFor5 = " " Then
            MsgBox("choose at least anything, please")
            Label9.Text = " "
            Label10.Text = " "
        ElseIf choiseFor5 = " " Or secondChoiseFor5 = " " Then
            MsgBox("choose at least anything, please")
            Label9.Text = " "
            Label10.Text = " "
        Else

            If secondChoiseFor5 = choiseFor5 Then
                MsgBox("in a draw")
                Label9.Text = name2 & " choise was " & secondChoiseFor5
                Label10.Text = name1 & " choise was " & choiseFor5
                nGames += 1

            ElseIf choiseFor5 = "rock" Then
                If secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "lizard" Then
                    MsgBox(name1 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "scissors" Then
                If secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Then
                    MsgBox(name1 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "papper" Then
                If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "Spock" Then
                    MsgBox(name1 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "lizard" Then
                If secondChoiseFor5 = "papper" Or secondChoiseFor5 = "Spock" Then
                    MsgBox(name1 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    loose += 1
                End If
            ElseIf choiseFor5 = "Spock" Then
                If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Then
                    MsgBox(name1 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    win += 1
                Else
                    MsgBox(name2 & " won")
                    Label9.Text = name2 & " choise was " & secondChoiseFor5
                    Label10.Text = name1 & " choise was " & choiseFor5
                    nGames += 1
                    loose += 1
                End If
            End If
        End If
        Label17.Text = name1 & vbCrLf & win
        Label18.Text = name2 & vbCrLf & loose
        If nGames = 10 Then
            MsgBox("Game Over" & vbCrLf & "your score: " & name1 & " " & win & " : " & name2 & " " & loose)
            win = 0
            loose = 0
            nGames = 0
        End If
        Start5_2()
    End Sub
    'user1 choise
    Private Sub RadioButton8_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton8.CheckedChanged
        choiseFor5 = "rock"

        RadioButton4.Checked = False
        RadioButton5.Checked = False
        RadioButton6.Checked = False
        RadioButton7.Checked = False
        RadioButton8.Checked = False
        RadioButton4.Visible = False
        RadioButton5.Visible = False
        RadioButton6.Visible = False
        RadioButton7.Visible = False
        RadioButton8.Visible = False
    End Sub
    Private Sub RadioButton7_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton7.CheckedChanged
        choiseFor5 = "scissors"

        RadioButton4.Checked = False
        RadioButton5.Checked = False
        RadioButton6.Checked = False
        RadioButton7.Checked = False
        RadioButton8.Checked = False
        RadioButton4.Visible = False
        RadioButton5.Visible = False
        RadioButton6.Visible = False
        RadioButton7.Visible = False
        RadioButton8.Visible = False
    End Sub
    Private Sub RadioButton6_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton6.CheckedChanged
        choiseFor5 = "papper"

        RadioButton4.Checked = False
        RadioButton5.Checked = False
        RadioButton6.Checked = False
        RadioButton7.Checked = False
        RadioButton8.Checked = False
        RadioButton4.Visible = False
        RadioButton5.Visible = False
        RadioButton6.Visible = False
        RadioButton7.Visible = False
        RadioButton8.Visible = False
    End Sub
    Private Sub RadioButton5_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton5.CheckedChanged
        choiseFor5 = "lizard"

        RadioButton4.Checked = False
        RadioButton5.Checked = False
        RadioButton6.Checked = False
        RadioButton7.Checked = False
        RadioButton8.Checked = False
        RadioButton4.Visible = False
        RadioButton5.Visible = False
        RadioButton6.Visible = False
        RadioButton7.Visible = False
        RadioButton8.Visible = False
    End Sub
    Private Sub RadioButton4_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton4.CheckedChanged
        choiseFor5 = "Spock"

        RadioButton4.Checked = False
        RadioButton5.Checked = False
        RadioButton6.Checked = False
        RadioButton7.Checked = False
        RadioButton8.Checked = False
        RadioButton4.Visible = False
        RadioButton5.Visible = False
        RadioButton6.Visible = False
        RadioButton7.Visible = False
        RadioButton8.Visible = False
    End Sub
    'user2 choise
    Private Sub RadioButton13_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton13.CheckedChanged
        secondChoiseFor5 = "rock"

        RadioButton9.Checked = False
        RadioButton10.Checked = False
        RadioButton11.Checked = False
        RadioButton12.Checked = False
        RadioButton13.Checked = False
        RadioButton9.Visible = False
        RadioButton10.Visible = False
        RadioButton11.Visible = False
        RadioButton12.Visible = False
        RadioButton13.Visible = False
    End Sub
    Private Sub RadioButton12_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton12.CheckedChanged
        secondChoiseFor5 = "scissors"

        RadioButton9.Checked = False
        RadioButton10.Checked = False
        RadioButton11.Checked = False
        RadioButton12.Checked = False
        RadioButton13.Checked = False
        RadioButton9.Visible = False
        RadioButton10.Visible = False
        RadioButton11.Visible = False
        RadioButton12.Visible = False
        RadioButton13.Visible = False
    End Sub
    Private Sub RadioButton11_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton11.CheckedChanged
        secondChoiseFor5 = "papper"

        RadioButton9.Checked = False
        RadioButton10.Checked = False
        RadioButton11.Checked = False
        RadioButton12.Checked = False
        RadioButton13.Checked = False
        RadioButton9.Visible = False
        RadioButton10.Visible = False
        RadioButton11.Visible = False
        RadioButton12.Visible = False
        RadioButton13.Visible = False
    End Sub
    Private Sub RadioButton10_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton10.CheckedChanged
        secondChoiseFor5 = "lizard"

        RadioButton9.Checked = False
        RadioButton10.Checked = False
        RadioButton11.Checked = False
        RadioButton12.Checked = False
        RadioButton13.Checked = False
        RadioButton9.Visible = False
        RadioButton10.Visible = False
        RadioButton11.Visible = False
        RadioButton12.Visible = False
        RadioButton13.Visible = False
    End Sub
    Private Sub RadioButton9_CheckedChanged(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles RadioButton9.CheckedChanged
        secondChoiseFor5 = "Spock"

        RadioButton9.Checked = False
        RadioButton10.Checked = False
        RadioButton11.Checked = False
        RadioButton12.Checked = False
        RadioButton13.Checked = False
        RadioButton9.Visible = False
        RadioButton10.Visible = False
        RadioButton11.Visible = False
        RadioButton12.Visible = False
        RadioButton13.Visible = False
    End Sub
    'clicks on pictures
    Private Sub PictureBox12_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox12.Click
        If choiseFor5 = "rock" Or choiseFor5 = "scissors" Or choiseFor5 = "papper" Or choiseFor5 = "lizard" Or choiseFor5 = "Spock" Then
            secondChoiseFor5 = "Spock"

            RadioButton9.Checked = False
            RadioButton10.Checked = False
            RadioButton11.Checked = False
            RadioButton12.Checked = False
            RadioButton13.Checked = False
            RadioButton9.Visible = False
            RadioButton10.Visible = False
            RadioButton11.Visible = False
            RadioButton12.Visible = False
            RadioButton13.Visible = False
            Button4_Click(sender, e)

        Else
            choiseFor5 = "Spock"

            RadioButton4.Checked = False
            RadioButton5.Checked = False
            RadioButton6.Checked = False
            RadioButton7.Checked = False
            RadioButton8.Checked = False
            RadioButton4.Visible = False
            RadioButton5.Visible = False
            RadioButton6.Visible = False
            RadioButton7.Visible = False
            RadioButton8.Visible = False
            If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Or secondChoiseFor5 = "Spock" Then
                Button4_Click(sender, e)
            End If
        End If
    End Sub
    Private Sub PictureBox13_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox13.Click
        If choiseFor5 = "rock" Or choiseFor5 = "scissors" Or choiseFor5 = "papper" Or choiseFor5 = "lizard" Or choiseFor5 = "Spock" Then
            secondChoiseFor5 = "lizard"

            RadioButton9.Checked = False
            RadioButton10.Checked = False
            RadioButton11.Checked = False
            RadioButton12.Checked = False
            RadioButton13.Checked = False
            RadioButton9.Visible = False
            RadioButton10.Visible = False
            RadioButton11.Visible = False
            RadioButton12.Visible = False
            RadioButton13.Visible = False
            Button4_Click(sender, e)

        Else
            choiseFor5 = "lizard"

            RadioButton4.Checked = False
            RadioButton5.Checked = False
            RadioButton6.Checked = False
            RadioButton7.Checked = False
            RadioButton8.Checked = False
            RadioButton4.Visible = False
            RadioButton5.Visible = False
            RadioButton6.Visible = False
            RadioButton7.Visible = False
            RadioButton8.Visible = False
            If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Or secondChoiseFor5 = "Spock" Then
                Button4_Click(sender, e)
            End If
        End If
    End Sub
    Private Sub PictureBox14_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox14.Click
        If choiseFor5 = "rock" Or choiseFor5 = "scissors" Or choiseFor5 = "papper" Or choiseFor5 = "lizard" Or choiseFor5 = "Spock" Then
            secondChoiseFor5 = "papper"

            RadioButton9.Checked = False
            RadioButton10.Checked = False
            RadioButton11.Checked = False
            RadioButton12.Checked = False
            RadioButton13.Checked = False
            RadioButton9.Visible = False
            RadioButton10.Visible = False
            RadioButton11.Visible = False
            RadioButton12.Visible = False
            RadioButton13.Visible = False
            Button4_Click(sender, e)

        Else
            choiseFor5 = "papper"

            RadioButton4.Checked = False
            RadioButton5.Checked = False
            RadioButton6.Checked = False
            RadioButton7.Checked = False
            RadioButton8.Checked = False
            RadioButton4.Visible = False
            RadioButton5.Visible = False
            RadioButton6.Visible = False
            RadioButton7.Visible = False
            RadioButton8.Visible = False
            If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Or secondChoiseFor5 = "Spock" Then
                Button4_Click(sender, e)
            End If
        End If
    End Sub
    Private Sub PictureBox15_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox15.Click
        If choiseFor5 = "rock" Or choiseFor5 = "scissors" Or choiseFor5 = "papper" Or choiseFor5 = "lizard" Or choiseFor5 = "Spock" Then
            secondChoiseFor5 = "scissors"

            RadioButton9.Checked = False
            RadioButton10.Checked = False
            RadioButton11.Checked = False
            RadioButton12.Checked = False
            RadioButton13.Checked = False
            RadioButton9.Visible = False
            RadioButton10.Visible = False
            RadioButton11.Visible = False
            RadioButton12.Visible = False
            RadioButton13.Visible = False
            Button4_Click(sender, e)

        Else
            choiseFor5 = "scissors"

            RadioButton4.Checked = False
            RadioButton5.Checked = False
            RadioButton6.Checked = False
            RadioButton7.Checked = False
            RadioButton8.Checked = False
            RadioButton4.Visible = False
            RadioButton5.Visible = False
            RadioButton6.Visible = False
            RadioButton7.Visible = False
            RadioButton8.Visible = False
            If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Or secondChoiseFor5 = "Spock" Then
                Button4_Click(sender, e)
            End If
        End If
    End Sub
    Private Sub PictureBox16_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles PictureBox16.Click
        If choiseFor5 = "rock" Or choiseFor5 = "scissors" Or choiseFor5 = "papper" Or choiseFor5 = "lizard" Or choiseFor5 = "Spock" Then
            secondChoiseFor5 = "rock"

            RadioButton9.Checked = False
            RadioButton10.Checked = False
            RadioButton11.Checked = False
            RadioButton12.Checked = False
            RadioButton13.Checked = False
            RadioButton9.Visible = False
            RadioButton10.Visible = False
            RadioButton11.Visible = False
            RadioButton12.Visible = False
            RadioButton13.Visible = False
            Button4_Click(sender, e)

        Else
            choiseFor5 = "rock"

            RadioButton4.Checked = False
            RadioButton5.Checked = False
            RadioButton6.Checked = False
            RadioButton7.Checked = False
            RadioButton8.Checked = False
            RadioButton4.Visible = False
            RadioButton5.Visible = False
            RadioButton6.Visible = False
            RadioButton7.Visible = False
            RadioButton8.Visible = False
            If secondChoiseFor5 = "rock" Or secondChoiseFor5 = "scissors" Or secondChoiseFor5 = "papper" Or secondChoiseFor5 = "lizard" Or secondChoiseFor5 = "Spock" Then
                Button4_Click(sender, e)
            End If
        End If
    End Sub

    'menu
    Private Sub btn_level_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_level.Click
        btn_level.Visible = False
        btn_easy.Visible = True
        btn_hard.Visible = True
    End Sub
    Private Sub btn_easy_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_easy.Click
        btn_easy.Visible = False
        btn_hard.Visible = False
        btn_e_pc.Visible = True
        btn_e_user.Visible = True
    End Sub
    Private Sub btn_hard_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_hard.Click
        btn_easy.Visible = False
        btn_hard.Visible = False
        btn_h_pc.Visible = True
        btn_h_user.Visible = True
    End Sub
    Private Sub btn_e_pc_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_e_pc.Click
        btn_e_pc.Visible = False
        btn_e_user.Visible = False
        Panel1.Visible = True 'easy user vs pc
        Panel4.Visible = False
        ToolStripMenuItem1.Visible = True 'hint
        panels()
    End Sub
    Private Sub btn_e_user_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_e_user.Click
        btn_e_pc.Visible = False
        btn_e_user.Visible = False
        'Panel2.Visible = True
        'Panel4.Visible = False
        'ToolStripMenuItem1.Visible = False

        'uvedení jmen
        Label19.Visible = True
        Label20.Visible = True
        Label21.Visible = True
        TextBox1.Visible = True
        TextBox2.Visible = True
        Button5.Visible = True
    End Sub
    Private Sub btn_h_pc_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_h_pc.Click
        btn_h_pc.Visible = False
        btn_h_user.Visible = False
        Panel3.Visible = True 'hard user vs pc
        Panel4.Visible = False
        ToolStripMenuItem1.Visible = True 'hint
        panels()

    End Sub
    Private Sub btn_h_user_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btn_h_user.Click
        btn_h_pc.Visible = False
        btn_h_user.Visible = False
        'Panel3.Visible = False
        'Panel4.Visible = False
        'Panel5.Visible = True
        'ToolStripMenuItem1.Visible = False

        'uvedení jmen
        Label19.Visible = True
        Label20.Visible = True
        Label21.Visible = True
        TextBox1.Visible = True
        TextBox2.Visible = True
        Button6.Visible = True
    End Sub

    'how to play
    Private Sub EasyToolStripMenuItem1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles EasyToolStripMenuItem1.Click
        MsgBox("Rock defeats Scissors." & vbCrLf & "Scissors defeats Papper. " & vbCrLf & "Papper defeats Rock." & vbCrLf & "Good luck! :) ")
    End Sub
    Private Sub HardToolStripMenuItem1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles HardToolStripMenuItem1.Click
        MsgBox("Rock defeats Scissors and Lizard." & vbCrLf & "Scissors defeats Papper and Lizard. " & vbCrLf & "Papper defeats Rock and Spock." & vbCrLf & "Lizard defeats Papper and Spock." & vbCrLf & "Spock defeats Scissors and Rock." & vbCrLf & "Good luck! :) ")
    End Sub

    'levels
    Private Sub UserVsComputerToolStripMenuItem3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles UserVsComputerToolStripMenuItem3.Click
        Panel1.Visible = True 'easy user vs pc
        Panel2.Visible = False
        Panel3.Visible = False
        Panel4.Visible = False
        Panel5.Visible = False
        win = 0
        loose = 0
        nGames = 0
        Label17.Text = " "
        Label18.Text = " "
        ToolStripMenuItem1.Visible = True
        Label2.Text = " "
        Label3.Text = " "
        Label5.Text = " "
        Label6.Text = " "
        Label12.Text = " "
        Label11.Text = " "
        Label9.Text = " "
        Label10.Text = " "
        panels()
    End Sub
    Private Sub UserToolStripMenuItem_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles UserToolStripMenuItem.Click
        If TextBox1.Text = "" Or TextBox2.Text = "" Then 'jestli jeste jmena nebyla uvedena
            'uvedení jmen
            Panel4.Visible = True 'menu
            Label19.Visible = True
            Label20.Visible = True
            Label21.Visible = True
            TextBox1.Visible = True
            TextBox2.Visible = True
            Button5.Visible = True
        Else
            Panel1.Visible = False
            Panel2.Visible = True
            Panel3.Visible = False
            Panel5.Visible = False
        End If

        Label7.Text = name1
        Label8.Text = name2
        userChoise = " "
        win = 0
        loose = 0
        nGames = 0
        Label17.Text = " "
        Label18.Text = " "
        ToolStripMenuItem1.Visible = False
        Label2.Text = " "
        Label3.Text = " "
        Label5.Text = " "
        Label6.Text = " "
        Label12.Text = " "
        Label11.Text = " "
        Label9.Text = " "
        Label10.Text = " "
    End Sub
    Private Sub UserVsComputerToolStripMenuItem4_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles UserVsComputerToolStripMenuItem4.Click
        Panel1.Visible = False
        Panel2.Visible = False
        Panel3.Visible = True 'hard user vs pc
        Panel4.Visible = False
        Panel5.Visible = False
        win = 0
        loose = 0
        nGames = 0
        Label17.Text = " "
        Label18.Text = " "
        ToolStripMenuItem1.Visible = True
        Label2.Text = " "
        Label3.Text = " "
        Label5.Text = " "
        Label6.Text = " "
        Label12.Text = " "
        Label11.Text = " "
        Label9.Text = " "
        Label10.Text = " "
        panels()

    End Sub
    Private Sub UserVsUserToolStripMenuItem3_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles UserVsUserToolStripMenuItem3.Click
        If TextBox1.Text = "" Or TextBox2.Text = "" Then 'jestle jeste jmena nebyla uvedena
            'uvedení jmen
            Panel4.Visible = True 'menu
            Label19.Visible = True
            Label20.Visible = True
            Label21.Visible = True
            TextBox1.Visible = True
            TextBox2.Visible = True
            Button6.Visible = True
        Else
            Panel1.Visible = False
            Panel2.Visible = False
            Panel3.Visible = False
            Panel5.Visible = True
        End If

        Label15.Text = name1
        Label16.Text = name2
        choiseFor5 = " "
        win = 0
        loose = 0
        nGames = 0
        Label17.Text = " "
        Label18.Text = " "
        ToolStripMenuItem1.Visible = False
        Label2.Text = " "
        Label3.Text = " "
        Label5.Text = " "
        Label6.Text = " "
        Label12.Text = " "
        Label11.Text = " "
        Label9.Text = " "
        Label10.Text = " "
    End Sub

    'hint
    Private Function help()
        Randomize()
        hint = CInt(Int((100 * Rnd()) + 1))
        Return hint
    End Function
    Private Sub ToolStripMenuItem1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles ToolStripMenuItem1.Click
        If Panel1.Visible = True Then
            RSP() 'získávání computerChoise
            If computerChoise = "rock" Then
                MsgBox("Scissors isn't a good idea.")
                ToolStripMenuItem1.Visible = False 'jen jedna nápověda za hru
            ElseIf computerChoise = "scissors" Then
                MsgBox("You'd better not choose papper.")
                ToolStripMenuItem1.Visible = False
            ElseIf computerChoise = "papper" Then
                MsgBox("Don't ever think about rock.")
                ToolStripMenuItem1.Visible = False
            End If
        ElseIf Panel3.Visible = True Then
            RSPLS() 'získávání computerChoise
            help() 'získávání hint
            If computerChoise = "rock" Then
                If hint < 50 Then
                    MsgBox("Scissors isn't a good idea.")
                    ToolStripMenuItem1.Visible = False
                Else
                    MsgBox("Lizard? Hmmm... no.")
                    ToolStripMenuItem1.Visible = False
                End If
            ElseIf computerChoise = "scissors" Then
                If hint < 50 Then
                    MsgBox("You'd better not choose papper.")
                    ToolStripMenuItem1.Visible = False
                Else
                    MsgBox("Definitely not lizard.")
                    ToolStripMenuItem1.Visible = False
                End If
            ElseIf computerChoise = "papper" Then
                If hint < 50 Then
                    MsgBox("Don't ever think about rock.")
                    ToolStripMenuItem1.Visible = False
                Else
                    MsgBox("Say no to Mr. Spock.")
                    ToolStripMenuItem1.Visible = False
                End If
            ElseIf computerChoise = "lizard" Then
                If hint < 50 Then
                    MsgBox("Remember, papper is bad.")
                    ToolStripMenuItem1.Visible = False
                Else
                    MsgBox("Don't touch Spock.")
                    ToolStripMenuItem1.Visible = False
                End If
            ElseIf computerChoise = "Spock" Then
                If hint < 50 Then
                    MsgBox("Don't do it. Don't choose rock.")
                    ToolStripMenuItem1.Visible = False
                Else
                    MsgBox("Not scissors.")
                    ToolStripMenuItem1.Visible = False
                End If
            End If
        End If

    End Sub
    'press enter
    Private Sub panels()
        If Panel1.Visible = True Then
            Me.AcceptButton = Button1
        ElseIf Panel3.Visible = True Then
            Me.AcceptButton = Button3
        End If
    End Sub

    'enter names
    Private Sub Button5_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button5.Click
        name1 = TextBox1.Text
        name2 = TextBox2.Text
        If TextBox1.Text = "" And TextBox2.Text = "" Then 'jestli uživatele nic neuvedli, mají jmena User 1 a User 2
            name1 = "User 1"
            name2 = "User 2"
        ElseIf TextBox1.Text = "" Then
            name1 = "User 1"
        ElseIf TextBox2.Text = "" Then
            name2 = "User 2"
        End If
        Panel1.Visible = False
        Panel2.Visible = True 'easy user vs user
        Panel3.Visible = False
        Panel4.Visible = False
        Panel5.Visible = False
        ToolStripMenuItem1.Visible = False
        Label19.Visible = False
        Label20.Visible = False
        Label21.Visible = False
        TextBox1.Visible = False
        TextBox2.Visible = False
        Button5.Visible = False
        Label7.Text = name1
        Label8.Text = name2
    End Sub
    Private Sub Button6_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button6.Click
        name1 = TextBox1.Text
        name2 = TextBox2.Text
        If TextBox1.Text = "" And TextBox2.Text = "" Then
            name1 = "User 1"
            name2 = "User 2"
        ElseIf TextBox1.Text = "" Then
            name1 = "User 1"
        ElseIf TextBox2.Text = "" Then
            name2 = "User 2"
        End If

        Panel1.Visible = False
        Panel2.Visible = False
        Panel3.Visible = False
        Panel4.Visible = False
        Panel5.Visible = True 'hard user vs user
        ToolStripMenuItem1.Visible = False
        Label19.Visible = False
        Label20.Visible = False
        Label21.Visible = False
        TextBox1.Visible = False
        TextBox2.Visible = False
        Button6.Visible = False
        Label15.Text = name1
        Label16.Text = name2
    End Sub
End Class